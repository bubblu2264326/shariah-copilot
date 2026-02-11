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
            'gemini-flash-latest',
            'gemini-2.0-flash',
            'gemini-1.5-pro',
            'gemini-2.5-flash',
        ]

    async def explain(self, clause_text: str, rule_text: str, status: str, metadata: dict = None, logic: str = None) -> dict:
        """Generates reasoning and suggested fixes for a compliance result with model fallbacks."""
        
        # Format metadata for the prompt
        metadata_str = json.dumps(metadata, indent=2) if metadata else "Not provided"
        
        prompt = f"""
        You are an elite Islamic Finance Compliance Officer and Sharia Auditor. Your goal is to provide a microscopic, rich-text audit of a Murabahah contract clause against AAOIFI standards.
        
        INPUT DATA:
        - Audited Contract Clause: "{clause_text}"
        - AAOIFI Sharia Standard: "{rule_text}"
        - System Verdict: {status}
        - Extracted Metadata: {metadata_str}
        - Compliance Logic: {logic if logic else "Not provided"}
        
        YOUR TASK:
        1. REASONING & DECISION TRACE: 
           - Provide a deep comparative analysis.
           - Explain EXACTLY how the Compliance Logic was applied to the Extracted Metadata.
           - If status is FAIL: Explicitly quote the problematic phrase using **bold** or > blockquotes. Explain exactly why the variables in the metadata (e.g., 'penalty_recipient') triggered a violation of the Sharia Standard.
           - If status is PASS: Use Markdown to highlight precisely how the contractual phrasing and metadata values align with AAOIFI requirements.
        
        2. SUGGESTION:
           - Provide the exact corrected contractual wording. Use Markdown code blocks (```) to encapsulate the suggested wording for clarity.
        
        OUTPUT FORMAT (JSON ONLY, NO FILLER):
        {{
            "reasoning": "Markdown formatted reasoning and logic trace...",
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
        
    async def deep_explain(self, target_node: dict, all_nodes: list, rule_text: str) -> dict:
        """Generates a deep, contextual explanation by looking at the entire contract sequence."""
        
        # Format the full context nicely for Gemini
        context_summary = []
        for node in all_nodes:
            status_icon = "✅" if node.get("status") == "PASS" else "❌"
            context_summary.append(f"- [{node.get('id')}] {status_icon} {node.get('topic')}: {node.get('original_text')[:100]}...")
            
        full_context_str = "\n".join(context_summary)
        
        prompt = f"""
        You are an elite Sharia Supervisory Board Member. You are performing a deep-dive audit review of a specific clause within the context of a FULL Murabahah contract lifecycle.
        
        TARGET CLAUSE TO EXPLAIN:
        - Topic: {target_node.get('topic')}
        - Content: "{target_node.get('original_text')}"
        - Extracted Metadata: {json.dumps(target_node.get('metadata'), indent=2)}
        - System Verdict: {target_node.get('status')}
        - AAOIFI Rule Reference: "{rule_text}"
        
        FULL CONTRACT CONTEXT (Cross-References):
        {full_context_str}
        
        YOUR TASK:
        1. CONTEXTUAL REASONING: 
           - Explain the decision for the target clause, but prioritize its relationship with the OTHER clauses listed in the context.
           - For example, if it's an Agency (Wakala) clause, explain how it interacts with the Possession or Sale clauses.
           - If it fails, specify if a contradiction exists BETWEEN clauses (e.g., selling before owning).
           
        2. SHARIA RATIONALE:
           - Provide the deeper "Maqasid al-Sharia" (intent/objective) behind this specific rule.
           - Don't just say 'it fails', say 'it undermines the risk-taking nature of trading'.
        
        OUTPUT FORMAT (JSON ONLY, NO FILLER):
        {{
            "deep_reasoning": "Rich Markdown formatted deep contextual analysis...",
            "sharia_foundations": "Markdown explanation of the underlying Sharia principles applicable here...",
            "inter_clause_conflicts": "List any specific IDs from the context that conflict with this clause, or null"
        }}
        """
        
        for model_name in self.model_names:
            try:
                self.logger.info(f"Attempting Deep Contextual Reasoning with model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                response = await asyncio.to_thread(model.generate_content, prompt)
                raw_text = response.text.strip()
                
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                clean_text = json_match.group(0) if json_match else raw_text

                if "```json" in clean_text:
                    clean_text = clean_text.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_text:
                    clean_text = clean_text.split("```")[1].split("```")[0].strip()
                    
                result = json.loads(clean_text)
                return result
                
            except Exception as e:
                self.logger.warning(f"Deep model {model_name} failed: {str(e)}. Attempting fallback...")
                continue
                
        return {
            "deep_reasoning": "Full contextual analysis unavailable due to technical connection limits.",
            "sharia_foundations": "Underlying principles can be found in AAOIFI Standard No. 8.",
            "inter_clause_conflicts": None
        }
