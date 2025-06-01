from pathlib import Path

# Fix trailing newlines
md_files = ["README.md", "KIMERA_SWM_READY.md"]
for md_file in md_files:
    if Path(md_file).exists():
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if not content.endswith('\n'):
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content + '\n')
            print(f"Fixed {md_file}")

# Create vault infrastructure
vault_dirs = ["vault", "vault/core", "vault/storage"]
for vault_dir in vault_dirs:
    Path(vault_dir).mkdir(parents=True, exist_ok=True)

init_files = ["vault/__init__.py", "vault/core/__init__.py", "vault/storage/__init__.py"]
for init_file in init_files:
    init_path = Path(init_file)
    if not init_path.exists():
        init_path.write_text('"""Vault module."""\n')

print("Quick fixes applied!")