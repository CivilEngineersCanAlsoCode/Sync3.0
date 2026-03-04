import argparse
import os
import json

def rank_bullets(bullets, jd_context):
    """
    Ranks bullets based on a composite score of Impact Magnitude and JD Alignment (PM-8uj).
    In a real scenario, this would call an LLM (Claude) to perform a semantic audit.
    For this implementation, we simulate the ranking logic.
    """
    # Placeholder for LLM-based semantic scoring
    # Logic: Score = (Impact Score 1-10) * (Alignment Score 1-10)
    ranked = []
    for bullet in bullets:
        # Simulate LLM scoring based on keywords and impact verbs
        impact_score = 5
        alignment_score = 5
        
        text = bullet.lower()
        # Impact detection
        if any(v in text for v in ["spearheaded", "architected", "delivered", "led", "saved", "increased"]):
            impact_score += 3
        if "%" in text or "$" in text or any(char.isdigit() for char in text):
            impact_score += 2
            
        # Alignment detection
        if any(kw in text for kw in jd_context.get("keywords", [])):
            alignment_score += 4
            
        composite_score = impact_score * alignment_score
        ranked.append({"text": bullet, "score": composite_score})
    
    # Sort by descending score
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return [item["text"] for item in ranked]

def draft_content(signals_json, jd_json, output_dir):
    """
    Drafts the filtered and prioritized content for a specific application.
    Implements Release 2 'Semantic Impact Ranking' (PM-8uj) and 'Temporal Weighting'.
    """
    with open(signals_json, 'r') as f:
        signals = json.load(f)
        
    with open(jd_json, 'r') as f:
        jd = json.load(f)
    
    # Contextual keywords for ranking
    jd_context = {
        "keywords": jd.get("required_skills", []) + jd.get("keyword_cluster", [])
    }

    application_content = {}
    
    # Process each role and prioritize bullets
    for role in signals.get("experience", []):
        company = role.get("company")
        bullets = role.get("bullets", [])
        
        # Release 2 Requirement: Intra-Project Prioritization
        prioritized_bullets = rank_bullets(bullets, jd_context)
        
        role_key = f"{company}_bullets"
        application_content[role_key] = prioritized_bullets

    # Summary and other metadata
    application_content["FULL_NAME"] = signals.get("name", "User")
    application_content["SUMMARY_LINE_1"] = "Simulated high-impact summary line matching JD."
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "content_draft.json")
    
    with open(output_path, 'w') as f:
        json.dump(application_content, f, indent=2)
        
    print(f"✅ Content drafted and prioritized: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draft prioritized resume content using Semantic Impact Ranking.")
    parser.add_argument("--signals", required=True, help="Path to high-precision signal JSON")
    parser.add_argument("--jd", required=True, help="Path to structured JD JSON")
    parser.add_argument("--output", required=True, help="Directory to save the draft")

    args = parser.parse_args()
    draft_content(args.signals, args.jd, args.output)
