import google.generativeai as genai
import json
import os
import logging
import asyncio

class ClauseExtractor:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger("clause_extractor")
        genai.configure(api_key=api_key)
        # Priority model list for fallback resilience
        self.model_names = [
            'gemini-flash-latest',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
            'gemini-2.5-flash',
        ]

    async def extract(self, pdf_bytes: bytes):
        """Extracts semantic clauses and their corresponding metadata values from a PDF with model fallbacks."""
        
        prompt = """
        You are an elite Islamic Finance Compliance Officer. Your task is to extract EVERY segment from this Murabaha contract that contains a functional requirement or legal commitment.
        
        DO NOT SUMMARIZE. Extract the raw text as it appears in the document.
        
        PART 1: SCANNING OBJECTIVES
        Find all sections related to:
        1. PRICING & PROFIT: How is the price determined? Is it fixed? Does it reference benchmarks (LIBOR, EIBOR)?
        2. PENALTIES: What happens if payment is late? Who receives the money?
        3. ASSET POSSESSION: When does the bank acquire the asset? When does the customer get it? Look for 'actual' or 'constructive' possession.
        4. AGENCY (WAKALA): Is the customer acting as an agent to buy the asset?
        5. INSURANCE/TAKAFUL: Who pays? Is it a condition?
        6. DISCOUNTS: Early payment discounts, etc.
        7. COSTS: Internal staff costs, administrative fees, etc.
        
        PART 2: STRUCTURED ANALYSIS
        For each extracted segment, perform a granular metadata analysis for the following variables:
        - clause_id: (The number or ID of the clause if found, e.g., '4.1', 'Clause 2', or null)
        - penalty_recipient: ('charity', 'bank', 'unknown')
        - profit_basis: ('fixed', 'future_variable', 'unknown')
        - is_fixed_at_signature: (true/false)
        - possession_acquired_before_sale: (true/false)
        - ownership_transfer_condition: ('immediate', 'on_full_payment', 'unknown')
        - customer_as_agent: (true/false)
        - dire_need_established: (true/false)
        - insurance_payer_pre_sale: ('bank', 'customer', 'unknown')
        - includes_internal_staff_costs: (true/false)
        - damage_recovery_includes_markup: (true/false)
        - discount_in_contract: (true/false)
        - price_increase_allowed_for_delay: (true/false)
        - bank_excludes_pre_existing_defects: (true/false)
        - expenses_disclosed: (true/false)
        - supplier_invoice_recipient: ('bank', 'customer', 'unknown')

        Output a JSON list of objects. Be exhaustive. Ensure EVERY object contains ALL metadata keys listed above.
        Format:
        [
          {
            "topic": "Identification of Topic",
            "clause_id": "4.1",
            "text": "Full verbatim text of the clause...",
            "metadata": { ...all variables above... }
          }
        ]
        """
        
        last_error = "Unknown error"
        for model_name in self.model_names:
            try:
                self.logger.info(f"Attempting PDF extraction with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Using to_thread for the blocking SDK call
                response = await asyncio.to_thread(
                    model.generate_content,
                    [prompt, {'mime_type': 'application/pdf', 'data': pdf_bytes}]
                )
                
                raw_text = response.text.strip()
                
                # JSON cleaning
                clean_text = raw_text
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()
                
                data = json.loads(clean_text)
                
                # Post-processing to ensure all keys exist for the rule engine
                default_metadata = {
                    "penalty_recipient": "unknown",
                    "profit_basis": "unknown",
                    "is_fixed_at_signature": True,
                    "possession_acquired_before_sale": True,
                    "ownership_transfer_condition": "immediate",
                    "customer_as_agent": False,
                    "dire_need_established": True,
                    "insurance_payer_pre_sale": "bank",
                    "includes_internal_staff_costs": False,
                    "damage_recovery_includes_markup": False,
                    "discount_in_contract": False,
                    "price_increase_allowed_for_delay": False,
                    "bank_excludes_pre_existing_defects": False,
                    "expenses_disclosed": True,
                    "supplier_invoice_recipient": "bank"
                }

                for item in data:
                    meta = item.get("metadata", {})
                    # Merge with defaults
                    item["metadata"] = {**default_metadata, **meta}
                    # Ensure clause_id exists
                    if "clause_id" not in item:
                        item["clause_id"] = None

                self.logger.info(f"Successfully parsed {len(data)} clauses using {model_name}.")
                return data, None
                
            except Exception as e:
                last_error = str(e)
                self.logger.warning(f"Model {model_name} failed: {last_error}. Attempting fallback...")
                continue
                
        self.logger.error("All Gemini models in fallback list failed for extraction.")
        return [], f"All models ({', '.join(self.model_names)}) failed: {last_error}"
