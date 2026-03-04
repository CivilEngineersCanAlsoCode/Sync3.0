import os
import subprocess
import json

def setup_sync():
    print("🚀 Initializing Sync Platform (Release 2.5)...")
    
    # 1. Beads Graph Initialization
    print("📦 Creating Beads Task Graph...")
    epic_cmd = ["bd", "create", "Sync Platform Release 2.5: Stability & Orchestration", "-t", "epic", "-p", "1", "--description", "Hardening the platform for production readiness."]
    epic_id = subprocess.check_output(epic_cmd).decode().strip().split()[-1]
    
    tasks = [
        ("Implement Horizontal Smart Trimmer", "PM-25a"),
        ("Implement Vertical Line Budgeting", "PM-25b"),
        ("Create Unified Pipeline Orchestrator", "PM-25c"),
        ("Add Assembly Safety Gate", "PM-25d"),
        ("Create One-Click Setup Script", "PM-25e"),
        ("Create requirements.txt", "PM-25f")
    ]
    
    for task_name, task_key in tasks:
        subprocess.run(["bd", "create", task_name, "-t", "task", "-p", "1", "--description", f"Resolving gap {task_key}."])
        # In a real run, we'd link them here
    
    subprocess.run(["bd", "sync"])
    print("✅ Beads graph initialized.")

    # 2. Environment Verification
    print("🔍 Verifying Environment...")
    try:
        import chromadb
        print("✅ ChromaDB found.")
    except ImportError:
        print("❌ ChromaDB missing. Run: pip install -r requirements.txt")

    print("\n✨ Setup Complete! You can now run the pipeline using:")
    print("python scripts/sync_main.py --jd [JD_PATH] --signals [SIGNALS_PATH]")

if __name__ == "__main__":
    setup_sync()
