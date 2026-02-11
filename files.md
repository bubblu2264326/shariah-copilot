# 📂 Project Structure: Murabaha Compliance Checker

This document explains the organization of files and folders in the project.

## 🏗️ Root Directory
- `backend/`: The FastAPI Python backend logic.
- `frontend/`: The Next.js 15 React frontend dashboard.
- `documentation/`: Detailed technical specs, PRDs, and logic documentation.
- `progress.md`: A living log of development milestones.

---

## 🐍 Backend (`/backend`)
- `main.py`: The entry point for the FastAPI server. Handles SSE (Real-time) streaming.
- `services/`:
  - `extractor.py`: Uses Gemini 1.5 Multimodal to extract clauses from PDFs.
  - `engine.py`: The "Hardcore" deterministic rule engine using `simpleeval`.
- `scripts/`:
  - `ingest_rules.py`: Ingests the 13 AAOIFI rules from JSON into the Pinecone Vector DB.
- `.venv/`: Python virtual environment containing dependencies.
- `.env`: **(Created by User)** Stores your Pinecone and Gemini API keys.
- `.env.example`: Template for environment variables.

---

## ⚛️ Frontend (`/frontend`)
- `src/app/`:
  - `page.tsx`: The main Dashboard UI (Upload, Progress, and Results).
  - `layout.tsx`: Root layout with premium fonts (Inter & Playfair Display).
  - `globals.css`: Tailwind CSS 4 configuration with the Emerald Green fintech theme.
- `src/components/ui/`: shadcn/ui components (Buttons, Cards, Tables, etc.).
- `src/lib/utils.ts`: Helper functions for Tailwind class merging.
- `package.json`: Frontend dependencies and startup scripts.

---

## 📜 Documentation (`/documentation`)
- `prd.md`: Product Requirements Document.
- `architecture.md`: Visual and technical system architecture.
- `logic_gates.md`: Detailed explanation of the 13 Sharia logic gates.
- `rules_extraction_report.md`: Summary of the 13 AAOIFI rules used.

---

## 🧠 Project Skill (`/.agent/skills/murabaha-compliance-checker`)
- `SKILL.md`: The "Technical Guardian" skill defining project rules.
- `references/murabaha_rules.json`: The **Master Rulebase** containing the exact 100% AAOIFI text and logic.
