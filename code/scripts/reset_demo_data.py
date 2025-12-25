#!/usr/bin/env python3
"""
Reset Demo Data Script
Author: OK Computer AI Agent
Version: 5.0.2

Reset demo data to clean state for out-of-box experience.
Append-only backup to data/_backup/<timestamp>/
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

def reset_demo_data(repo_root: str = "."):
    """Reset demo data with backup."""
    
    repo_path = Path(repo_root)
    data_path = repo_path / "data"
    
    # Create backup directory
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = data_path / "_backup" / timestamp
    backup_path.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Backup directory: {backup_path}")
    
    # Directories to backup
    directories_to_backup = [
        "event_store",
        "quarantine", 
        "audit",
        "kpi_pulse",
        "scenario"
    ]
    
    for dir_name in directories_to_backup:
        source_dir = data_path / dir_name
        backup_dir = backup_path / dir_name
        
        if source_dir.exists():
            print(f"📁 Backing up {dir_name}...")
            if source_dir.is_file():
                # If it's a file, create parent directory
                backup_dir.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source_dir), str(backup_dir))
            else:
                # If it's a directory
                shutil.move(str(source_dir), str(backup_dir))
        else:
            print(f"⚠️  {dir_name} not found, skipping...")
    
    # Create clean directories
    print("\n🧹 Creating clean data directories...")
    
    # Event store
    event_store_dir = data_path / "event_store"
    event_store_dir.mkdir(exist_ok=True)
    (event_store_dir / "event_log.jsonl").touch()
    (event_store_dir / "idempotency_keys.txt").touch()
    
    # Quarantine
    quarantine_dir = data_path / "quarantine"
    quarantine_dir.mkdir(exist_ok=True)
    (quarantine_dir / "quarantine_events.jsonl").touch()
    
    # Audit
    (data_path / "audit").mkdir(exist_ok=True)
    
    # KPI pulse
    (data_path / "kpi_pulse").mkdir(exist_ok=True)
    
    # Scenario
    (data_path / "scenario").mkdir(exist_ok=True)
    
    print("✅ Demo data reset completed!")
    print(f"📂 Backup location: {backup_path}")
    print("🚀 Ready for out-of-box demo!")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Reset demo data with backup")
    parser.add_argument("--repo_root", default=".", help="Repository root directory")
    
    args = parser.parse_args()
    reset_demo_data(args.repo_root)
