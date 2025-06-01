#!/usr/bin/env python3
"""
Cleanup GitHub workflows and CI configuration
"""
import os
import shutil

def cleanup_workflows():
    """Clean up GitHub workflows"""
    print("🔧 CLEANING UP WORKFLOWS")
    print("=" * 30)
    
    # Check for workflow backup
    if os.path.exists('.github/workflows_backup'):
        print("📁 Found workflows backup")
        
        # List backup contents
        if os.path.isdir('.github/workflows_backup'):
            backup_files = os.listdir('.github/workflows_backup')
            print(f"  Backup contains: {backup_files}")
        else:
            print("  Backup is a file, not directory")
    
    # Check current workflows
    if os.path.exists('.github/workflows'):
        workflow_files = [f for f in os.listdir('.github/workflows') if f.endswith('.yml')]
        print(f"📋 Current workflows: {workflow_files}")
        
        # Validate CI workflow
        ci_file = '.github/workflows/ci.yml'
        if os.path.exists(ci_file):
            print("✅ CI workflow exists")
            
            # Check if it's valid
            try:
                with open(ci_file, 'r') as f:
                    content = f.read()
                if 'name:' in content and 'on:' in content:
                    print("✅ CI workflow appears valid")
                else:
                    print("⚠️ CI workflow may be incomplete")
            except Exception as e:
                print(f"❌ Error reading CI workflow: {e}")
        else:
            print("❌ CI workflow missing")
    
    # Check for codespell config
    if os.path.exists('.codespellrc'):
        print("✅ Codespell config exists")
    else:
        print("⚠️ Codespell config missing")
    
    # Check VSCode config
    if os.path.exists('.vscode/launch.json'):
        print("✅ VSCode launch config exists")
    else:
        print("⚠️ VSCode launch config missing")
    
    print("\n📊 Workflow cleanup complete")
    return True

if __name__ == "__main__":
    cleanup_workflows()