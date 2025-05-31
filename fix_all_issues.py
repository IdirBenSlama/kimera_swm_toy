#!/usr/bin/env python3
"""
One-shot script to fix all remaining issues in Kimera-SWM v0.7.0
Addresses:
1. Unicode emoji crashes in PowerShell
2. pandas dependency for demos
3. pytest async warnings
4. Command line parsing issues
"""

import sys
import os
from pathlib import Path

def fix_demo_unicode_issues():
    """Replace Unicode emojis with ASCII equivalents in demo files."""
    print("Fixing Unicode emoji issues in demo files...")
    
    # Unicode to ASCII mapping
    emoji_map = {
        "🎯": "[TARGET]",
        "📦": "[PACKAGE]", 
        "✅": "[OK]",
        "❌": "[ERROR]",
        "📂": "[FOLDER]",
        "🔬": "[ANALYSIS]",
        "📊": "[METRICS]",
        "🔄": "[PROCESSING]",
        "📈": "[CHART]",
        "📄": "[REPORT]",
        "🎉": "[SUCCESS]",
        "🔐": "[SECURE]",
        "🏹": "[ARROW]",
        "🧪": "[TEST]"
    }
    
    demo_files = [
        "demo_metrics_safe.py",
        "demo_metrics.py",
        "cache_demo.py"
    ]
    
    for demo_file in demo_files:
        if Path(demo_file).exists():
            print(f"  Fixing {demo_file}...")
            with open(demo_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace emojis
            for emoji, ascii_equiv in emoji_map.items():
                content = content.replace(emoji, ascii_equiv)
            
            with open(demo_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"    [OK] Fixed Unicode issues in {demo_file}")

def add_pytest_async_markers():
    """Add pytest async markers to test files."""
    print("Adding pytest async markers...")
    
    test_files = [
        "tests/test_openai_async.py",
        "tests/test_reactor.py",
        "tests/test_reactor_mp.py"
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"  Checking {test_file}...")
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if pytest mark is already present
            if "pytestmark = pytest.mark.asyncio" not in content:
                # Add the marker after imports
                lines = content.split('\n')
                insert_pos = 0
                
                # Find position after imports
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        insert_pos = i + 1
                    elif line.strip() and not line.strip().startswith('#'):
                        break
                
                # Insert the marker
                lines.insert(insert_pos, "")
                lines.insert(insert_pos + 1, "# Mark all tests in this file as async")
                lines.insert(insert_pos + 2, "pytestmark = pytest.mark.asyncio")
                lines.insert(insert_pos + 3, "")
                
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                print(f"    [OK] Added async marker to {test_file}")
            else:
                print(f"    [OK] Async marker already present in {test_file}")

def create_powershell_friendly_runner():
    """Create a PowerShell-friendly script runner."""
    print("Creating PowerShell-friendly runner...")
    
    runner_content = '''#!/usr/bin/env python3
"""
PowerShell-friendly runner for Kimera benchmarks.
Handles Unicode issues and provides clear command examples.
"""

import sys
import os
import subprocess
from pathlib import Path

def run_safe_demo():
    """Run the safe metrics demo with ASCII output."""
    print("[INFO] Running Kimera metrics demo (ASCII mode)...")
    try:
        result = subprocess.run([
            sys.executable, "demo_metrics_safe.py"
        ], capture_output=True, text=True, encoding='utf-8', errors='replace')
        
        print(result.stdout)
        if result.stderr:
            print("[STDERR]", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Demo failed: {e}")
        return False

def run_benchmark_with_stats():
    """Run benchmark with comprehensive stats."""
    print("[INFO] Running benchmark with metrics...")
    
    # Check for API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-proj-"):
        print("[WARNING] No valid API key found. Running Kimera-only mode.")
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare",
            "data/contradictions_2k.csv",
            "--max-pairs", "500",
            "--stats",
            "--no-cache",
            "--kimera-only"
        ]
    else:
        cmd = [
            sys.executable, "-m", "benchmarks.llm_compare", 
            "data/contradictions_2k.csv",
            "--max-pairs", "500", 
            "--stats",
            "--no-cache",
            "--async", "8",
            "--mp", "4"
        ]
    
    try:
        print(f"[CMD] {' '.join(cmd)}")
        result = subprocess.run(cmd, encoding='utf-8', errors='replace')
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Benchmark failed: {e}")
        return False

def run_tests():
    """Run pytest with proper configuration."""
    print("[INFO] Running test suite...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "-v", "--tb=short"
        ], encoding='utf-8', errors='replace')
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Tests failed: {e}")
        return False

def main():
    """Main runner with menu."""
    print("Kimera-SWM v0.7.0 PowerShell-Friendly Runner")
    print("=" * 50)
    print()
    print("Available commands:")
    print("1. demo     - Run safe metrics demo")
    print("2. benchmark - Run full benchmark with stats")
    print("3. test     - Run test suite")
    print("4. all      - Run everything")
    print()
    
    if len(sys.argv) < 2:
        choice = input("Enter choice (1-4): ").strip()
    else:
        choice = sys.argv[1]
    
    success = True
    
    if choice in ["1", "demo"]:
        success = run_safe_demo()
    elif choice in ["2", "benchmark"]:
        success = run_benchmark_with_stats()
    elif choice in ["3", "test"]:
        success = run_tests()
    elif choice in ["4", "all"]:
        print("Running complete validation...")
        success = (
            run_safe_demo() and
            run_tests() and
            run_benchmark_with_stats()
        )
    else:
        print(f"[ERROR] Unknown choice: {choice}")
        success = False
    
    if success:
        print()
        print("[SUCCESS] All operations completed successfully!")
        print()
        print("Generated files:")
        for file in ["kimera_metrics_demo.png", "kimera_metrics_demo.yaml", 
                    "benchmark_results.csv", "metrics.yaml", "roc.png"]:
            if Path(file).exists():
                print(f"  - {file}")
    else:
        print()
        print("[ERROR] Some operations failed. Check output above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open("run_powershell_safe.py", 'w', encoding='utf-8') as f:
        f.write(runner_content)
    print("  [OK] Created run_powershell_safe.py")

def create_ascii_demo():
    """Create an ASCII-only version of the demo."""
    print("Creating ASCII-only demo...")
    
    # Read the current demo
    if Path("demo_metrics_safe.py").exists():
        with open("demo_metrics_safe.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create ASCII version
        ascii_content = content.replace("🎯", "[TARGET]")
        ascii_content = ascii_content.replace("📦", "[PACKAGE]")
        ascii_content = ascii_content.replace("✅", "[OK]")
        ascii_content = ascii_content.replace("❌", "[ERROR]")
        ascii_content = ascii_content.replace("📂", "[FOLDER]")
        ascii_content = ascii_content.replace("🔬", "[ANALYSIS]")
        ascii_content = ascii_content.replace("📊", "[METRICS]")
        ascii_content = ascii_content.replace("🔄", "[PROCESSING]")
        ascii_content = ascii_content.replace("📈", "[CHART]")
        ascii_content = ascii_content.replace("📄", "[REPORT]")
        ascii_content = ascii_content.replace("🎉", "[SUCCESS]")
        ascii_content = ascii_content.replace("🔐", "[SECURE]")
        
        with open("demo_metrics_ascii.py", 'w', encoding='utf-8') as f:
            f.write(ascii_content)
        print("  [OK] Created demo_metrics_ascii.py")

def verify_dependencies():
    """Verify all required dependencies are installed."""
    print("Verifying dependencies...")
    
    required_packages = [
        "pandas", "numpy", "scikit-learn", "matplotlib", 
        "pytest", "pytest-asyncio", "pyyaml"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"  [OK] {package}")
        except ImportError:
            missing.append(package)
            print(f"  [ERROR] {package} (missing)")
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Run: poetry install")
        return False
    
    return True

def main():
    """Main fix script."""
    print("Kimera-SWM v0.7.0 - Fixing All Issues")
    print("=" * 40)
    print()
    
    # Check if we're in the right directory
    if not Path("src/kimera").exists():
        print("[ERROR] Not in Kimera project root directory")
        return 1
    
    try:
        # 1. Fix Unicode issues
        fix_demo_unicode_issues()
        print()
        
        # 2. Add pytest markers
        add_pytest_async_markers()
        print()
        
        # 3. Create PowerShell runner
        create_powershell_friendly_runner()
        print()
        
        # 4. Create ASCII demo
        create_ascii_demo()
        print()
        
        # 5. Verify dependencies
        deps_ok = verify_dependencies()
        print()
        
        if deps_ok:
            print("[OK] All fixes applied successfully!")
            print()
            print("Next steps:")
            print("1. Run: python run_powershell_safe.py demo")
            print("2. Run: python run_powershell_safe.py test")
            print("3. Run: python run_powershell_safe.py benchmark")
            print()
            print("Or run everything: python run_powershell_safe.py all")
        else:
            print("[WARNING] Fixes applied but dependencies missing")
            print("Run 'poetry install' first")
        
        return 0
        
    except Exception as e:
        print(f"[ERROR] Fix script failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())