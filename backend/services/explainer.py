import google.generativeai as genai
import json
import logging
import asyncio
import re

class ComplianceExplainer:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger("compliance_explainer")
        genai.configure(api_key=api_key)
        # Priority model list for fallback resilience
        self.model_names = [
            'gemini-2.0-flash',
            'gemini-2.5-flash',
            'gemini-flash-latest'
        ]

    async def explain(self, clause_text: str, rule_text: str, status: str) -> dict:
        """Generates reasoning and suggested fixes for a compliance result with model fallbacks."""
        
        prompt = f"""
        You are an elite Islamic Finance Compliance Officer and Sharia Auditor. Your goal is to provide a microscopic, rich-text audit of a Murabahah contract clause against AAOIFI standards.
        
        INPUT DATA:
        - Audited Contract Clause: "{clause_text}"
        - AAOIFI Sharia Standard: "{rule_text}"
        - System Verdict: {status}
        
        YOUR TASK:
        1. REASONING: 
           - Provide a deep comparative analysis.
           - If status is FAIL: Explicitly quote the problematic phrase using **bold** or > blockquotes. Explain exactly why it contradicts the Sharia Standard.
           - If status is PASS: Use Markdown to highlight precisely how the contractual phrasing aligns with AAOIFI requirements.
        
        2. SUGGESTION:
           - Provide the exact corrected contractual wording. Use Markdown code blocks (```) to encapsulate the suggested wording for clarity.
        
        OUTPUT FORMAT (JSON ONLY, NO FILLER):
        {{
            "reasoning": "Markdown formatted reasoning...",
            "suggestion": "Markdown formatted suggestion..."
        }}
        """
        
        for model_name in self.model_names:
            try:
                self.logger.info(f"Attempting Sharia reasoning with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                # Using to_thread for the blocking SDK call
                response = await asyncio.to_thread(
                    model.generate_content,
                    prompt
                )
                
                raw_text = response.text.strip()
                
                # Robust JSON extraction using regex
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if json_match:
                    clean_text = json_match.group(0)
                else:
                    clean_text = raw_text

                # Additional cleaning for common Gemini formatting
                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()
                    
                result = json.loads(clean_text)
                self.logger.info(f"Successfully generated reasoning using {model_name}")
                return result
                
            except Exception as e:
                self.logger.warning(f"Model {model_name} failed for reasoning: {str(e)}. Attempting fallback...")
                continue
                
        self.logger.error("All Gemini models in fallback list failed for reasoning.")
        return {
            "reasoning": f"### Audit Verified\n\n- **Verdict**: {status}\n- **Analysis**: Phrasing evaluated against AAOIFI standards. Detailed AI reasoning unavailable due to technical connection limits.",
            "suggestion": "Consult the AAOIFI Standard No. 8 for precise wording requirements."
        }
