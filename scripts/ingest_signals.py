import argparse
import os
import json
import chromadb

def ingest_career_signals(signals_json, db_path):
    """
    Ingests career signals into a local persistent ChromaDB with hierarchical chunking (PM-9e5).
    Every chunk is self-contained with context: "What did you do at [Company] as [Role]?"
    """
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("career_signals")
    
    with open(signals_json, 'r') as f:
        data = json.load(f)
    
    documents = []
    metadatas = []
    ids = []
    
    for role in data.get("experience", []):
        company = role.get("company")
        title = role.get("role")
        duration = role.get("duration")
        
        for i, bullet in enumerate(role.get("bullets", [])):
            # PM-9e5: Hierarchical self-contained chunk
            # Context is embedded IN the document text for maximum LLM retrieval relevance
            contextual_text = f"Context: {company} | Role: {title} ({duration})\nAchievement: {bullet}"
            
            documents.append(contextual_text)
            metadatas.append({
                "company": company,
                "role": title,
                "type": "impact_bullet",
                "index": i
            })
            ids.append(f"{company}_{title}_{i}".replace(" ", "_"))

    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    print(f"✅ Ingested {len(ids)} hierarchical signals into {db_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest hierarchical career signals into local ChromaDB.")
    parser.add_argument("--signals", required=True, help="Path to raw career signals JSON")
    parser.add_argument("--db", default="./.chroma_db", help="Path to local ChromaDB persistence")

    args = parser.parse_args()
    ingest_career_signals(args.signals, args.db)
