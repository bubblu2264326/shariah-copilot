---
name: murabaha-compliance-checker
description: Expert in Murabaha AAOIFI compliance checking. Handles PDF ingestion, Sharia rule matching via Pinecone, and Gemini-based reasoning. Use when working on the Murabaha AI Compliance Checker project, processing Sharia standards, or implementing compliance logic for Islamic banking.
---

# Murabaha Compliance Checker

## Overview

This skill enables the development and operation of an AI-powered compliance checker for Murabaha contracts, specifically aligned with AAOIFI FAS 28 standards. It covers the end-to-end pipeline from PDF extraction to deterministic logic-gate verification and LLM-based explanation.

### 1. Project Overview
The Murabaha AI Compliance Checker is a production-grade system that verifies Islamic banking contracts against AAOIFI FAS 28 standards.

### 2. Mandatory Maintenance Rules (CRITICAL)
- **Update Progress**: You MUST update `progress.md` after every user request to reflect what was accomplished, any changes in technical state, and the next milestone.
- **Technical Guardianship**: Always update `documentation/technical_choices.md` and `documentation/architecture.md` immediately if there is an architectural pivot (e.g., changing from Gemini Embeddings to Pinecone Inference).
- **Production Readiness**: All code and configurations must be production-ready (env-variable driven, proper error handling, direct deployment capable). Use `pnpm` for all frontend operations.

## Core Capabilities

### 1. Sharia Rule Repository (FAS 28)
- Managed via `references/murabaha_rules.json`.
- Rules are embedded and stored in Pinecone for semantic retrieval.
- Keywords: `penalty-as-income`, `ownership-risk`, `deferred-payment`, `commodity-murabaha`.

### 2. PDF Processing & Clause Extraction
- Uses layout-aware parsing (Marker/Unstructured) to maintain document structure.
- Splits contracts into logical clauses for granular compliance checks.

### 3. Compliance Logic Gates (Rule Engine)
- Rules are loaded from `references/murabaha_rules.json`.
- Dynamic evaluator runs boolean logic strings (e.g., `profit_basis == 'future_variable'`).
- Severity levels: `critical`, `warning`, `notice`.

### 4. Explainable AI (XAI)
- Uses Gemini 1.5 Pro to provide citations and simple explanations for compliance verdicts.

## Implementation Workflow

### Step 1: Data Structuring
Extract rules from `Shariaa-Standards-ENG.pdf` and convert to JSON format.
[Example Rule JSON](file:///home/oops/projects/hackathon/documentation/prd.md#L30)

### Step 2: Vector DB Sync
Run scripts to sync the JSON rulebase to Pinecone.

### Step 3: Backend Ingestion
Implement FastAPI endpoints for PDF upload and streaming results.

### Step 4: Frontend Visualization
Build React components for the live compliance dashboard.

## Resources

### references/
- `murabaha_rules.json`: Canonical list of FAS 28 rules.
- `architecture.md`: Detailed system design.

### scripts/
- `extract_rules.py`: Scrapes PDF for FAS 28 rules.
- `sync_pinecone.py`: Updates Pinecone index.
- `process_contract.py`: Core logic for clause analysis.

### assets/
- `sample_murabaha_contract.pdf`: For testing.
- `frontend_boilerplate/`: Next.js starters.
