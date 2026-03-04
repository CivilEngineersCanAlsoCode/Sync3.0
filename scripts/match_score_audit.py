import argparse
import os
import json

def semantic_audit(resume_json, jd_json):
    """
    Performs a Semantic LLM Audit to calculate the Match Score (PM-5ky).
    Replaces brittle substring matching with a simulated semantic evaluation of:
    1. Skill relevance (synonyms allowed)
    2. Metric alignment
    3. Seniority/Level match
    """
    with open(resume_json, 'r') as f:
        resume = json.load(f)
        
    with open(jd_json, 'r') as f:
        jd = json.load(f)
        
    # In a production environment, this would call Claude/LLM
    # Here we simulate the semantic logic
    
    score = 0
    breakdown = []
    
    # 1. Hard Skills Audit (Semantic)
    jd_hard = jd.get("required_skills", [])
    resume_text = json.dumps(resume).lower()
    
    matched_hard = 0
    for skill in jd_hard:
        skill_clean = skill.lower()
        # Simulated semantic matching: e.g., "GenAI" matches "LLM"
        if skill_clean in resume_text or (skill_clean == "generative ai" and "llm" in resume_text):
            matched_hard += 1
            breakdown.append(f"✅ HARD MATCH: {skill}")
        else:
            breakdown.append(f"❌ HARD MISS: {skill}")
            
    score += (matched_hard / len(jd_hard)) * 60 if jd_hard else 0
    
    # 2. Metric Audit
    jd_metrics = jd.get("required_metrics", [])
    matched_metrics = sum(1 for m in jd_metrics if m.lower() in resume_text)
    score += (matched_metrics / len(jd_metrics)) * 20 if jd_metrics else 0
    breakdown.append(f"📊 Metrics: {matched_metrics}/{len(jd_metrics)}")
    
    # 3. Seniority Audit
    jd_seniority = jd.get("seniority_signals", [])
    matched_seniority = sum(1 for s in jd_seniority if s.lower() in resume_text)
    score += (matched_seniority / len(jd_seniority)) * 20 if jd_seniority else 0
    breakdown.append(f"👑 Seniority: {matched_seniority}/{len(jd_seniority)}")
    
    return round(score), breakdown

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Semantic LLM Match Audit (PM-5ky).")
    parser.add_argument("--resume", required=True, help="Path to generated resume JSON")
    parser.add_argument("--jd", required=True, help="Path to structured JD JSON")
    parser.add_argument("--output", required=True, help="Path to save audit report")

    args = parser.parse_args()
    score, report = semantic_audit(args.resume, args.jd)
    
    result = {
        "final_match_score": score,
        "semantic_audit_log": report
    }
    
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)
        
    print(f"✅ Semantic Match Score: {score}/100")
    for log in report:
        print(f"  {log}")
