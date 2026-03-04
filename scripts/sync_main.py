import argparse
import os
import json
import sys

# Import our specialized scripts as modules
from ingest_signals import ingest_career_signals
from query_signals import query_signals
from draft_content import draft_content
from assemble import assemble_resume
from match_score_audit import semantic_audit

def calculate_vertical_load(content):
    """
    PM-25b: Vertical Line Budgeting.
    Header: 4 lines
    Role Headers: 2 lines each
    Bullets: 1 line each
    Spacer: 1 line
    """
    total_lines = 4 # Header + Tagbar
    # Simplified estimation
    for key, val in content.items():
        if "_bullets" in key:
            total_lines += 2 # Role header
            total_lines += len(val) # Bullets
    return total_lines

def enforce_line_budget(content, limit=62):
    """
    If the vertical load exceeds the limit, remove bullets from the oldest roles.
    """
    load = calculate_vertical_load(content)
    if load <= limit:
        return content
        
    print(f"⚠️ Vertical Load ({load}) exceeds budget ({limit}). Trimming bullets...")
    
    # Sort roles to find the oldest (this is a simplification, in production we'd use dates)
    role_keys = [k for k in content.keys() if "_bullets" in k]
    # We'll just reverse and pop from the last one found for now
    while calculate_vertical_load(content) > limit and role_keys:
        target_role = role_keys[-1]
        if content[target_role]:
            content[target_role].pop() # Remove a bullet
        else:
            role_keys.pop() # Role is empty, move to next
            
    return content

def run_pipeline(jd_path, signals_path, template_path, output_dir):
    db_path = "./.chroma_db"
    
    print("🚀 Starting Sync Pipeline Orchestrator...")
    
    # 1. Ingest (if needed - usually happens once, but we verify)
    ingest_career_signals(signals_path, db_path)
    
    # 2. Query
    retrieved = query_signals(jd_path, db_path)
    retrieved_path = os.path.join(output_dir, "retrieved_signals.json")
    with open(retrieved_path, 'w') as f:
        json.dump(retrieved, f)
        
    # 3. Draft & Prioritize
    draft_content(signals_path, jd_path, output_dir)
    draft_path = os.path.join(output_dir, "content_draft.json")
    
    # 4. PM-25b: Load draft and apply Vertical Line Budgeting
    with open(draft_path, 'r') as f:
        content = json.load(f)
    
    budgeted_content = enforce_line_budget(content)
    with open(draft_path, 'w') as f:
        json.dump(budgeted_content, f, indent=2)
        
    # 5. Assemble
    resume_output = os.path.join(output_dir, "resume.html")
    assemble_resume(template_path, draft_path, resume_output)
    
    # 6. Audit
    score, report = semantic_audit(draft_path, jd_path)
    print(f"✅ Pipeline Complete! Match Score: {score}/100")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Unified Pipeline Orchestrator (Release 2.5).")
    parser.add_argument("--jd", required=True, help="Path to structured JD JSON")
    parser.add_argument("--signals", required=True, help="Path to career signals JSON")
    parser.add_argument("--template", default="Templates/Base_Template.html", help="Path to HTML template")
    parser.add_argument("--output-dir", default="./Output", help="Directory for generated artifacts")

    args = parser.parse_args()
    run_pipeline(args.jd, args.signals, args.template, args.output_dir)
