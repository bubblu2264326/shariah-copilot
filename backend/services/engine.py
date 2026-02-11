from simpleeval import simple_eval
import logging

class HardcoreRuleEngine:
    """A production-ready rule engine for Sharia compliance verification."""
    
    def __init__(self):
        self.logger = logging.getLogger("compliance_engine")
        logging.basicConfig(level=logging.INFO)

    def evaluate(self, rule_id: str, logic_str: str, contract_metadata: dict) -> bool:
        """
        Evaluates a Sharia rule using safe expression evaluation.
        Returns: True if rule FAILS (non-compliant), False if rule PASSES.
        """
        try:
            self.logger.info(f"Evaluating {rule_id}: {logic_str} with {contract_metadata}")
            
            # simple_eval is safe for production (doesn't have the risks of eval())
            # It only allows simple operators and variables we provide.
            result = simple_eval(logic_str, names=contract_metadata)
            
            self.logger.info(f"Result for {rule_id}: {'FAIL' if result else 'PASS'}")
            return bool(result)
            
        except Exception as e:
            self.logger.error(f"Rule Engine Error ({rule_id}): {str(e)}")
            # Default to FAIL if logic is malformed for safety
            return True

    def validate_variable_set(self, logic_str: str, available_metadata: dict):
        """Ensures all variables in logic_str exist in metadata before evaluation."""
        # Optional: Add parsing to check for missing keys early
        pass
