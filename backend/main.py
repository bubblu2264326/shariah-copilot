import os
import json
import asyncio
from typing import List
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pinecone import Pinecone
from dotenv import load_dotenv

import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    force=True
)
logger = logging.getLogger("api")

from services.extractor import ClauseExtractor
from services.engine import HardcoreRuleEngine
from services.explainer import ComplianceExplainer

# Load environment variables
load_dotenv()

# Initialize APIs
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("murabaha-rules")

# Initialize Services
extractor = ClauseExtractor(api_key=GOOGLE_API_KEY)
engine = HardcoreRuleEngine()
explainer = ComplianceExplainer(api_key=GOOGLE_API_KEY)

app = FastAPI(title="Murabaha Compliance Audit Engine")

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_contract(file: UploadFile = File(...)):
    """Primary SSE endpoint for production-grade Sharia compliance analysis."""
    
    async def event_generator():
        # 1. READ FILE
        yield f"data: {json.dumps({'status': 'processing', 'message': 'Successfully received file. Reading content...'})}\n\n"
        pdf_bytes = await file.read()
        
        # 2. EXTRACT CLAUSES
        yield f"data: {json.dumps({'status': 'processing', 'message': 'AI is analyzing document structure...'})}\n\n"
        await asyncio.sleep(0.5)
        yield f"data: {json.dumps({'status': 'processing', 'message': 'Extracting semantic Murabaha clauses...'})}\n\n"
        
        # Start heartbeat task for better UX
        heartbeat_msg = ["Synthesizing Sharia intent...", "Mapping legal cross-references...", "Verifying AAOIFI compliance nodes..."]
        
        clauses_task = asyncio.create_task(extractor.extract(pdf_bytes))
        
        i = 0
        while not clauses_task.done():
            yield f"data: {json.dumps({'status': 'processing', 'message': heartbeat_msg[i % len(heartbeat_msg)]})}\n\n"
            await asyncio.sleep(2)
            i += 1
            
        clauses, error_msg = await clauses_task
        
        if error_msg:
            logger.error(f"Extraction failed: {error_msg}")
            yield f"data: {json.dumps({'status': 'error', 'message': error_msg})}\n\n"
            return
            
        if not clauses:
            logger.warning("Gemini Extractor returned 0 clauses.")
            yield f"data: {json.dumps({'status': 'error', 'message': 'AI Protocol Failure: No sharia-critical clauses identified in document.'})}\n\n"
            return
            
        # Add index-based ID for frontend synchronization
        for idx, clause in enumerate(clauses):
            clause["id"] = f"cl_{idx}"

        # PHASE 1: Send all extracted clauses to the frontend immediately
        yield f"data: {json.dumps({'status': 'clauses_extracted', 'data': clauses})}\n\n"

        # PHASE 2 & 3: ANALYZE EACH CLAUSE SEQUENTIALLY
        for clause in clauses:
            yield f"data: {json.dumps({'status': 'retrieving', 'message': f'Cross-referencing {clause['topic']}...'})}\n\n"
            
            # Semantic search in Pinecone
            query_embedding = pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[clause["text"]],
                parameters={"input_type": "query"}
            )
            
            search_results = index.query(
                vector=query_embedding[0].values,
                top_k=1,
                include_metadata=True
            )
            
            if search_results.matches:
                match = search_results.matches[0]
                rule_meta = match.metadata
                
                # Dynamic Logic Evaluation (Hardcore Engine)
                is_fail = engine.evaluate(match.id, rule_meta["logic"], clause["metadata"])
                status_verdict = "FAIL" if is_fail else "PASS"
                
                # PHASE 2: Send verdict and truth immediately
                verdict_data = {
                    "id": clause["id"],
                    "rule_id": match.id,
                    "topic": rule_meta["topic"],
                    "status": status_verdict,
                    "severity": rule_meta["severity"],
                    "citation": rule_meta["citation"],
                    "exact_rule_text": rule_meta["rule_text"],
                    "original_text": clause["text"],
                    "clause_id": clause.get("clause_id", None)
                }
                yield f"data: {json.dumps({'status': 'verdict', 'data': verdict_data})}\n\n"
                
                # PHASE 3: Generate and stream AI reasoning
                yield f"data: {json.dumps({'status': 'processing', 'message': f'Synthesizing reasoning for {clause['topic']}...'})}\n\n"
                ai_details = await explainer.explain(
                    clause_text=clause["text"],
                    rule_text=rule_meta["rule_text"],
                    status=status_verdict
                )
                
                reasoning_data = {
                    "id": clause["id"],
                    "explanation": ai_details.get("reasoning", rule_meta["rule_summary"]),
                    "reasoning": ai_details.get("reasoning", ""),
                    "suggestion": ai_details.get("suggestion", "")
                }
                yield f"data: {json.dumps({'status': 'reasoning', 'data': reasoning_data})}\n\n"
            
            # Slight sleep for smoother frontend streaming
            await asyncio.sleep(0.3)

        yield f"data: {json.dumps({'status': 'complete', 'message': 'Full Audit Complete.'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
