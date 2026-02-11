import google.generativeai as genai
import json
import os
import logging

class ClauseExtractor:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger("clause_extractor")
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash for balanced speed/intelligence
        self.model = genai.GenerativeModel('gemini-flash-latest')

    async def extract(self, pdf_bytes: bytes):
        """Extracts semantic clauses and their corresponding metadata values from a PDF."""
        
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
        - penalty_recipient: ('charity', 'bank', 'unknown')
        - profit_basis: ('fixed', 'future_variable', 'unknown')
        - is_fixed_at_signature: (true/false)
        - possession_acquired_before_sale: (true/false)
        - ownership_transfer_condition: ('immediate', 'on_full_payment', 'unknown')
        - customer_as_agent: (true/false)
        - insurance_payer_pre_sale: ('bank', 'customer', 'unknown')
        - includes_internal_staff_costs: (true/false)
        - damage_recovery_includes_markup: (true/false)
        - discount_in_contract: (true/false)
        - expenses_disclosed: (true/false)
        - supplier_invoice_recipient: ('bank', 'customer', 'unknown')

        Output a JSON list of objects. Be exhaustive. If there are many clauses, extract all of them.
        Format:
        [
          {
            "topic": "Identification of Topic",
            "text": "Full verbatim text of the clause...",
            "metadata": { ...all variables above... }
          }
        ]
        """
        
        try:
            # We use the parts API for high-quality multimodal input
            self.logger.info("Sending PDF to Gemini for extraction...")
            response = self.model.generate_content([
                prompt,
                {'mime_type': 'application/pdf', 'data': pdf_bytes}
            ])
            
            raw_text = response.text.strip()
            self.logger.info(f"Raw Gemini Response: {raw_text}")
            
            # Robust JSON cleaning
            clean_text = raw_text
            if "```json" in clean_text:
                clean_text = clean_text.split("```json")[1].split("```")[0].strip()
            elif "```" in clean_text:
                clean_text = clean_text.split("```")[1].split("```")[0].strip()
            
            self.logger.info(f"Cleaned JSON Text: {clean_text}")
            results = json.loads(clean_text)
            self.logger.info(f"Successfully parsed {len(results)} clauses.")
            return results
        except Exception as e:
            self.logger.error(f"Gemini Extraction error: {str(e)}")
            return []
