# 📜 Extraction Report: Murabaha Rules (SS 8)

I have performed a deep-read of **AAOIFI Shari'ah Standard No. (8): Murabahah** (Pages 195-231). Below is the summary of the clauses extracted for our vector database.

## 🏁 Rulebase Summary

The following rules have been structured into `murabaha_rules.json` for the Pinecone index:

1.  **MUR-001: Penalty as Charity** (Clause 5/6)
    *   *Rule*: Late fees must go to charity, not bank profit.
2.  **MUR-002: Fixed Profit/LIBOR Prohibition** (Clause 4/6)
    *   *Rule*: Profit cannot be tied to future variable rates (like LIBOR) in the final sale.
3.  **MUR-003: Possession Before Sale** (Clause 3/1/1)
    *   *Rule*: Bank must own/possess asset before selling.
4.  **MUR-004: Ownership Transfer Timing** (Clause 5/4)
    *   *Rule*: Ownership cannot be withheld until full payment.
5.  **MUR-005: Agency Restriction** (Clause 3/1/3)
    *   *Rule*: Customer shouldn't be agent unless "dire need."
6.  **MUR-006: Hamish Jiddiyyah (Damage Recovery)** (Clause 2/5/3)
    *   *Rule*: Only actual damage (cost diff) can be taken from deposit, not profit.
7.  **MUR-007: Insurance Responsibility** (Clause 3/2/6)
    *   *Rule*: Bank pays for insurance as long as it owns the asset.
8.  **MUR-008: Early Payment Rebate** (Clause 5/9)
    *   *Rule*: Rebates are allowed but cannot be a contractual right/obligation.
9.  **MUR-009: Price Increase Prohibition** (Clause 4/8)
    *   *Rule*: Debt amount is fixed; cannot increase price for extra time.
10. **MUR-010: Defect Responsibility** (Clause 4/10)
    *   *Rule*: Bank is liable for hidden defects appearing after contract but before delivery.
11. **MUR-011: Expense Disclosure** (Clause 4/3)
    *   *Rule*: Full transparency required; all added expenses must be disclosed.
12. **MUR-012: Documentation Name** (Clause 3/1/6)
    *   *Rule*: Supplier documents must be in the bank's name to prove asset purchase.
13. **MUR-013: Direct Expenses Only** (Clause 4/4)
    *   *Rule*: Prohibition of hidden charges or internal staff costs in the Murabaha price.

## 🛠️ Developer Guidance
*   **Embeddings**: Embed the `rule_text` for high semantic similarity.
*   **Context**: Use the `citation` in the frontend UI to link users back to the AAOIFI PDF.
*   **Logic**: Use the `logic_gate` field to drive the deterministic compliance checks.
