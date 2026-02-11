# 🎙️ Sharia Copilot: Murabaha AI Compliance Checker

> **Automating Sharia Audits with Generative AI | PROCOM '26 Hackathon**

[![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Google_Gemini-3_Pro-blue?style=flat-square&logo=google-gemini)](https://ai.google.dev/)
[![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-blueviolet?style=flat-square&logo=pinecone)](https://www.pinecone.io/)

Sharia Copilot is an AI-powered compliance engine designed to transform the Sharia audit process for Islamic banking. Developed for the PROCOM '26 Hackathon, it specifically targets **Murabaha contracts**, ensuring they adhere to **AAOIFI FAS 28** standards with speed and precision.

---

## 🛑 The Problem
Sharia compliance is often the slowest link in the Islamic banking pipeline. Auditing 100+ page contracts against thousands of pages of AAOIFI standards is:
- **Manual & Tedious**: High cognitive load on auditors.
- **Error-Prone**: Fatigue leads to missed non-compliance risks (e.g., "Penalty as Income").
- **Unscalable**: Human-only auditing cannot keep up with growing portfolios.

## 💡 The Solution
Sharia Copilot reduces audit turnaround from **hours to seconds**. By combining **Deterministic Logic Gates** with **Generative AI Deep Reasoning**, it provides a 100% clause-by-clause evaluation that auditors can trust.

---

## ✨ Key Features
- 🚀 **Real-time Streaming**: Watch the AI analyze clauses instantly as it reads the document.
- 🧠 **Deep Reasoning**: Explains *why* a clause fails with direct citations and comparative Sharia analysis.
- 🎨 **Premium UI**: Executive-level dark-mode glassmorphic dashboard built for clarity.
- 🔎 **Focus Mode**: Granular views for investigating specific clause-rule conflicts.

---

## ⚙️ Intelligent Pipeline
The system operates on a 4-stage autonomous engine:
1.  **Ingestion**: High-fidelity PDF extraction and semantic segmentation.
2.  **Retrieval (RAG)**: Pinecone Vector DB matches clauses to authorized AAOIFI Standards.
3.  **Governance**: Deterministic logic gates filter for hard violations.
4.  **Deep Reasoning**: Google Gemini 3 Pro provides nuanced, multi-clause interpretation.

---

## 🛠️ The Modern Stack
- **Frontend**: Next.js 15, Framer Motion, Radix UI.
- **Backend**: FastAPI (Python 3.12).
- **AI/ML**: Google Gemini 1.5 Pro, Gemini Text Embeddings (text-embedding-004).
- **Database**: Pinecone (Vectorized Sharia Knowledge Base).

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ & Python 3.10+
- [Vercel CLI](https://vercel.com/download) (for deployment)
- API Keys for **Google Gemini** and **Pinecone**.

### Environment Setup
Create a `.env` file in the `backend/` directory:
```env
PINECONE_API_KEY=your_pinecone_key
GOOGLE_API_KEY=your_gemini_key
```

### Installation & Local Development

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/bubblu2264326/shariah-copilot.git
   cd shariah-copilot
   ```

2. **Run Backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Run Frontend**:
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

---

## 📄 Project Structure
```text
.
├── backend/            # FastAPI Server & AI Services
│   ├── services/       # Compliance logic & LLM wrappers
│   └── vercel.json     # Deployment config
├── frontend/           # Next.js Web Dashboard
│   ├── components/     # Premium Glassmorphic UI
│   └── app/            # Next.js App Router
├── documentation/      # PRD, Architecture, & Pitch Deck
└── README.md           # You are here
```

---

## 🏆 Hackathon Context
This project was built as a functional MVP for the **PROCOM '26 Hackathon**. It demonstrates how AI-First banking can maintain Sharia integrity at Silicon Valley speed.

---

*Sharia integrity meets Generative AI speed.*
