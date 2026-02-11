# 🧠 JSON-Driven Logic Engine

To ensure scalability and maintainability, our compliance checker uses a **JSON-Driven Engine**. Rules are not hard-coded in Python; they are loaded from `murabaha_rules.json` and evaluated dynamically.

## The Flow

1.  **Selection**: The system retrieves relevant rules from Pinecone based on the clause text.
2.  **Metadata Extraction (AI)**: Gemini extracts the specific `variables` defined in the retrieved rule.
3.  **Dynamic Evaluation (Code)**: A simple Python evaluator runs the `logic` string against the extracted metadata.
4.  **Verdict Application**:
    *   **FAIL**: If `logic` evaluates to `True`, the `fail_message` is returned with the rule's `severity`.
    *   **OK**: If all checks pass.

## Example: Rule MUR-002 (LIBOR)
*   **Rule Logic**: `"profit_basis == 'future_variable' or is_fixed_at_signature == false"`
*   **Extracted Info**: `{"profit_basis": "future_variable", "is_fixed_at_signature": true}`
*   **Engine Result**: `True` → **CRITICAL FAIL**

## Severity Levels
*   🔴 **Critical**: Absolute Sharia prohibition (e.g., Riba, Possession issues).
*   🟡 **Warning**: Strong recommendation or discouragement (e.g., Mixed agency).
*   🔵 **Notice**: Transparency or documentation improvement suggested.

## Benefits
*   **Zero-Code Updates**: Add a new rule by just dropping a JSON entry.
*   **Explainability**: Every result points to a `citation`, a `logic`, and a specific `fail_message`.
*   **Auditability**: Every extraction and logic result is logged.
