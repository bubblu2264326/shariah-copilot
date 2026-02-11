import os
import json
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "murabaha-rules"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

def ingest_rules():
    # 1. Create Index if it doesn't exist
    if INDEX_NAME not in pc.list_indexes().names():
        print(f"Creating index {INDEX_NAME}...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=1024, # Dimension for multilingual-e5-large
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    
    index = pc.Index(INDEX_NAME)

    # 2. Load rules from JSON
    rules_path = "/home/oops/projects/hackathon/.agent/skills/murabaha-compliance-checker/references/murabaha_rules.json"
    print(f"Loading rules from: {rules_path}")
    with open(rules_path, "r") as f:
        rules = json.load(f)

    print(f"Loaded {len(rules)} rules. Starting ingestion...")

    # 3. Process and Upload
    vectors = []
    
    # We use Pinecone Inference for embeddings
    # Model: multilingual-e5-large
    texts = [rule["rule_text"] for rule in rules]
    
    print("Generating embeddings using Pinecone Inference...")
    embeddings = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=texts,
        parameters={"input_type": "passage"}
    )

    for i, rule in enumerate(rules):
        vectors.append({
            "id": rule["rule_id"],
            "values": embeddings[i].values,
            "metadata": {
                "topic": rule["topic"],
                "rule_summary": rule["rule_summary"],
                "citation": rule["citation"],
                "rule_text": rule["rule_text"], # Exact words
                "logic": rule["logic"],
                "severity": rule["severity"]
            }
        })

    # 4. Upsert to Pinecone
    print(f"Upserting {len(vectors)} vectors to Pinecone...")
    index.upsert(vectors=vectors)
    print("Ingestion complete! Rulebase is now searchable.")

if __name__ == "__main__":
    if not PINECONE_API_KEY:
        print("Error: PINECONE_API_KEY not found in .env")
    else:
        ingest_rules()
