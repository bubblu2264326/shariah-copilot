# Technical Choices & Proposed Architecture: Murabaha AI Compliance Checker

This document outlines the key technical decisions and options for the Murabaha AI Compliance Checker to ensure a robust, hackathon-ready implementation.

## 1. Vector Database: Why Pinecone?
The user requested Pinecone.
* **Pro**: Serverless, easy to scale, free tier available.
* **Con**: Limited metadata filtering on free tier (but sufficient for MVP).
* **Alternatives**: 
    * **Milvus/Zilliz**: High performance, but more complex setup.
    * **Supabase (pgvector)**: Excellent if we were already using Supabase for the database.
* **Decision**: Stay with **Pinecone** for simplicity and user preference.

## 2. Core AI Components
*   **Vector Database**: **Pinecone (Free Tier)**.
    *   **Embeddings Generation**: **Pinecone Inference** (Free tier offers 5M tokens/month). This keeps our Vector DB and Inference in one place.
    *   **LLM (Reasoning & Extraction)**: **Gemini 1.5 Pro/Flash** (via API) for multi-modal parsing and final compliance explanations.

## 3. PDF Parsing Strategy
* **Recommendation**: **Option C (Gemini Multimodal)** for best data quality, as these documents are legal and need high accuracy.

## 4. Streaming: SSE vs WebSockets
* **Decision**: **Server-Sent Events (SSE)**. 
    * **Simpler Implementation**: Lightweight and native to HTTP.
    * **One-Way Delivery**: Perfect for sending live analysis updates from backend to frontend.
    * **Automatic Reconnection**: Built into the SSE standard.

## 5. UI/UX Design
* **Decision**: **Modern FinTech Sleek**.
    * **Theme**: Support for both **Dark and Light modes**.
    * **Aesthetic**: Glassmorphism, smooth micro-animations, Inter font.
    * **Color Palette**: Emerald Green accents (professional/Islamic) on a sophisticated charcoal/white background.
