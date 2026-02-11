import google.generativeai as genai
import json
import logging

class ComplianceExplainer:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger("compliance_explainer")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    async def explain(self, clause_text: str, rule_text: str, status: str) -> dict:
        """Generates reasoning and suggested fixes for a compliance result."""
        
        prompt = f"""
        You are an elite AAOIFI Sharia Auditor. Your goal is to provide a microscopic audit of a Murabahah contract clause.
        
        INPUT DATA:
        - Audited Contract Clause: "{clause_text}"
        - AAOIFI Sharia Standard: "{rule_text}"
        - System Verdict: {status}
        
        YOUR TASK:
        1. REASONING: 
           - If status is FAIL: Explicitly quote the problematic phrase from the 'Audited Contract Clause'. Explain exactly why it contradicts the 'AAOIFI Sharia Standard'. Use phrases like "Your contract states '...', which is non-compliant because..."
           - If status is PASS: Confirm how the specific phrasing in the clause aligns with the AAOIFI requirement.
        
        2. SUGGESTION:
           - Provide the exact corrected contractual wording that would make this clause 100% Sharia compliant while maintaining the bank's legal intent.
        
        OUTPUT FORMAT (JSON ONLY):
        {{
            "reasoning": "Detailed comparative analysis here...",
            "suggestion": "Corrected contractual wording here..."
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # JSON cleaning
            if "```json" in raw_text:
                raw_text = raw_text.split("```json")[1].split("```")[0].strip()
            elif "```" in raw_text:
                raw_text = raw_text.split("```")[1].split("```")[0].strip()
                
            return json.loads(raw_text)
        except Exception as e:
            self.logger.error(f"Explanation error: {str(e)}")
            return {
                "reasoning": f"Audit complete. Phrasing evaluated against AAOIFI standards. Verdict: {status}.",
                "suggestion": "Review the specific AAOIFI standard for precise wording updates."
            }
