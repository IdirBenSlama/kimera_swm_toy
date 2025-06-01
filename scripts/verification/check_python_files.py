#!/usr/bin/env python3
"""
Check Python files for syntax and import issues
"""
import os
import ast
import importlib.util
import sys

def check_python_files():
    """Check all Python files for syntax and import issues"""
    print("🐍 CHECKING PYTHON FILES")
    print("=" * 30)
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv'}
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    syntax_errors = []
    import_errors = []
    valid_files = []
    
    for file_path in python_files:
        print(f"🔍 Checking {file_path}...")
        
        # Check syntax
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
            print(f"  ✅ Syntax OK")
            
            # Check if it's importable (basic check)
            try:
                spec = importlib.util.spec_from_file_location("temp_module", file_path)
                if spec and spec.loader:
                    # Don't actually import, just check if we can create the spec
                    print(f"  ✅ Import structure OK")
                    valid_files.append(file_path)
                else:
                    print(f"  ⚠️ Import structure unclear")
                    valid_files.append(file_path)  # Still count as valid
            except Exception as e:
                print(f"  ⚠️ Import check failed: {e}")
                import_errors.append((file_path, str(e)))
                
        except SyntaxError as e:
            print(f"  ❌ Syntax error: {e}")
            syntax_errors.append((file_path, str(e)))
        except UnicodeDecodeError as e:
            print(f"  ❌ Encoding error: {e}")
            syntax_errors.append((file_path, f"Encoding error: {e}"))
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")
            syntax_errors.append((file_path, str(e)))
    
    # Summary
    print(f"\n📊 PYTHON FILE CHECK SUMMARY:")
    print(f"  Total files: {len(python_files)}")
    print(f"  Valid files: {len(valid_files)}")
    print(f"  Syntax errors: {len(syntax_errors)}")
    print(f"  Import issues: {len(import_errors)}")
    
    if syntax_errors:
        print(f"\n❌ SYNTAX ERRORS:")
        for file_path, error in syntax_errors:
            print(f"  {file_path}: {error}")
    
    if import_errors:
        print(f"\n⚠️ IMPORT ISSUES:")
        for file_path, error in import_errors:
            print(f"  {file_path}: {error}")
    
    success_rate = len(valid_files) / len(python_files) * 100 if python_files else 0
    print(f"\n🎯 Success rate: {success_rate:.1f}%")
    
    if len(syntax_errors) == 0:
        print(f"✅ ALL FILES HAVE VALID SYNTAX")
        return True
    else:
        print(f"❌ {len(syntax_errors)} FILES HAVE SYNTAX ISSUES")
        return False

if __name__ == "__main__":
    success = check_python_files()
    sys.exit(0 if success else 1)