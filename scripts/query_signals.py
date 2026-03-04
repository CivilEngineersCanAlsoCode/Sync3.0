import argparse
import os
import json
import chromadb

def query_signals(jd_json, db_path, n_results=3):
    """
    Performs multi-angle retrieval (PM-9pv) to ensure diverse and high-precision career signals.
    Issues 3 separate queries:
    1. Hard Skills
    2. Metric Types
    3. Seniority/Leadership Signals
    """
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("career_signals")
    
    with open(jd_json, 'r') as f:
        jd = json.load(f)
    
    # PM-9pv: Multi-Angle Query Vectors
    queries = {
        "hard_skills": ", ".join(jd.get("required_skills", [])),
        "metrics": ", ".join(jd.get("required_metrics", [])),
        "seniority": ", ".join(jd.get("seniority_signals", []))
    }
    
    all_results = []
    seen_ids = set()
    
    for angle, query_text in queries.items():
        if not query_text.strip():
            continue
            
        print(f"🔍 Issuing {angle} query: {query_text[:50]}...")
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        
        # Deduplicate results using seen_ids
        for i, doc_id in enumerate(results['ids'][0]):
            if doc_id not in seen_ids:
                seen_ids.add(doc_id)
                all_results.append({
                    "id": doc_id,
                    "text": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "angle": angle
                })
                
    return all_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-angle career signal retrieval (Release 2).")
    parser.add_argument("--jd", required=True, help="Path to structured JD JSON")
    parser.add_argument("--db", default="./.chroma_db", help="Path to local ChromaDB persistence")
    parser.add_argument("--output", required=True, help="Path to save retrieved signals")

    args = parser.parse_args()
    retrieved = query_signals(args.jd, args.db)
    
    with open(args.output, 'w') as f:
        json.dump(retrieved, f, indent=2)
        
    print(f"✅ Retrieved {len(retrieved)} high-precision signals across all angles.")
