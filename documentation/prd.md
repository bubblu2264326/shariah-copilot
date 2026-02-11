# 🏗️ PRD: Murabaha AI Compliance Checker (Hackathon MVP)

## 1️⃣ Project Goal
Build a **fully functional web app** that allows Islamic banks to **verify Murabaha contracts** against AAOIFI Shariah standards (FAS 28). The system will:
* Ingest a **PDF contract**
* Extract all **clauses**
* Check them against **all Murabaha-related rules in AAOIFI FAS 28**
* Show **real-time progress and results**
* Provide **explainable compliance verdicts** (OK / FAIL) for each clause

## 2️⃣ Scope
* **Product Type:** Murabaha
* **Rule Coverage:** **All rules related to Murabaha** in AAOIFI FAS 28
* **Frontend + Backend:** Full demo
* **Vector DB:** Pinecone (supports free embeddings via OpenAI / Gemini API)
* **LLM:** Gemini API (for clause extraction, reasoning, and explanation)
* **Tech Stack:** Next.js (frontend) + FastAPI (backend) + Pinecone (vector DB)

## 3️⃣ Functional Requirements
### 3.1 User Flow
1. User uploads **Murabaha contract PDF**
2. Backend converts PDF → **plain text**
3. Text is **split into clauses** (headings, sentences)
4. Each clause is **embedded using Gemini embeddings**
5. Embedded clauses are matched with **Murabaha rules vector database (Pinecone)**
6. LLM (Gemini) assists in **reasoning/explanation**
7. Backend applies **hard-coded logic rules** → verdict per clause (`OK / FAIL`)
8. Frontend shows:
   * **Loading bar with progress**
   * **Real-time updates on clause analysis**
   * **Results table:** clause, related rule, verdict, explanation, source citation

### 3.2 Data Model (Rules JSON Structure)
```json
{
  "rule_id": "MUR-001",
  "topic": "Penalty as income",
  "rule_summary": "Penalty cannot be treated as bank income",
  "rule_text": "Full AAOIFI text from FAS 28, Clause X",
  "citation": "AAOIFI FAS 28, Clause X",
  "logic_gate": "IF penalty_as_income == true THEN FAIL",
  "keywords": ["penalty", "income", "non-compliant"],
  "source_url": "https://aaoifi.com/shariah-standards/"
}
```

### 3.3 Backend Requirements
* **Tech:** FastAPI
* **Responsibilities:** PDF conversion, clause extraction, Gemini integration, Pinecone query, logic-based checks, streaming.

### 3.4 Frontend Requirements
* **Tech:** Next.js
* **Responsibilities:** Upload PDF, progress/status UI, results table.

## 4️⃣ Non-Functional Requirements
* **Performance:** Support ~50 page PDFs.
* **Responsiveness:** Live clause-by-clause updates.
* **Reliability:** Authoritative AAOIFI source.

## 5️⃣ Responsible AI & Risks
* **Risk:** Hallucination in interpretation. 
* **Mitigation:** Use hard-coded logic gates + direct citation mapping to reduce reliance on LLM for final verdict.
* **Constraint:** Deterministic verdicts for known rules.
