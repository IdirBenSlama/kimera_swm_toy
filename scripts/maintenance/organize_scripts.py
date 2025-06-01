#!/usr/bin/env python3
"""
Organize scripts into functional categories
"""
import os
import shutil
import glob

def organize_scripts():
    """Organize scripts by function"""
    print("📁 ORGANIZING SCRIPTS BY FUNCTION")
    print("=" * 40)
    
    # Create directories if they don't exist
    script_dirs = [
        "scripts/development",
        "scripts/testing", 
        "scripts/verification",
        "scripts/maintenance"
    ]
    
    for dir_path in script_dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Created {dir_path}")
    
    # Define script categories
    categories = {
        'development': [
            'demo_*.py', 'execute_*.py', 'quick_*.py', 'simple_*.py',
            'basic_*.py', 'final_*.py', 'minimal_*.py', 'setup_*.py',
            'scar_demo.py'
        ],
        'testing': [
            'run_*.py', 'test_*.py'
        ],
        'verification': [
            'check_*.py', 'verify_*.py', 'validate_*.py'
        ],
        'maintenance': [
            'fix_*.py', 'cleanup_*.py', 'organize_*.py', 
            'move_*.py', 'batch_*.py'
        ]
    }
    
    moved_counts = {cat: 0 for cat in categories}
    
    # Get all Python files in root
    root_scripts = glob.glob('*.py')
    
    for script in root_scripts:
        # Skip certain files
        skip_files = {
            'conftest.py', 'pyproject.toml', '__init__.py',
            'execute_complete_reorganization.py',
            'verify_traceability_reorganization.py',
            'run_traceability_reorganization.py'
        }
        
        if script in skip_files:
            continue
        
        moved = False
        for category, patterns in categories.items():
            for pattern in patterns:
                if script.startswith(pattern.replace('*', '')) or \
                   (pattern.endswith('*.py') and script.startswith(pattern[:-3])):
                    target_dir = f"scripts/{category}"
                    target_path = f"{target_dir}/{script}"
                    
                    if not os.path.exists(target_path):
                        shutil.move(script, target_path)
                        print(f"📦 Moved {script} → {target_dir}/")
                        moved_counts[category] += 1
                        moved = True
                        break
            if moved:
                break
        
        if not moved:
            print(f"⚠️ {script} - no category match")
    
    # Summary
    total_moved = sum(moved_counts.values())
    print(f"\n📊 SCRIPT ORGANIZATION SUMMARY:")
    print(f"  Total scripts moved: {total_moved}")
    
    for category, count in moved_counts.items():
        if count > 0:
            print(f"  📁 {category}: {count} scripts")
    
    # List current organization
    print(f"\n📋 CURRENT ORGANIZATION:")
    for dir_path in script_dirs:
        if os.path.exists(dir_path):
            scripts = [f for f in os.listdir(dir_path) if f.endswith('.py')]
            print(f"  📁 {dir_path}: {len(scripts)} scripts")
            for script in scripts[:3]:  # Show first 3
                print(f"    • {script}")
            if len(scripts) > 3:
                print(f"    ... and {len(scripts) - 3} more")
    
    return total_moved

if __name__ == "__main__":
    organize_scripts()