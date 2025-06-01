"""
Test Configuration for Kimera Test Suite
========================================

Configuration settings and constants for the test suite.
"""

from pathlib import Path

# Test Configuration
TEST_CONFIG = {
    # Timeout settings (in seconds)
    "timeouts": {
        "quick_test": 30,
        "integration_test": 60,
        "full_test": 120
    },
    
    # Required files and directories
    "required_structure": {
        "directories": [
            "src",
            "src/kimera", 
            "vault",
            "vault/core",
            ".github/workflows"
        ],
        "files": [
            "src/kimera/__init__.py",
            "src/kimera/identity.py",
            "src/kimera/storage.py", 
            "src/kimera/reactor_mp.py",
            "vault/__init__.py",
            "vault/core/__init__.py",
            "vault/core/vault.py",
            ".github/workflows/ci.yml"
        ]
    },
    
    # Test files to run
    "test_files": {
        "quick": [
            "test_import_fixes.py",
            "test_system_quick.py", 
            "basic_import_test.py"
        ],
        "ci_simulation": [
            "test_import_fixes.py",
            "test_system_quick.py",
            "test_vault_and_scar.py"
        ]
    },
    
    # Known issues to ignore (phantom errors)
    "ignore_patterns": [
        # Spelling warnings for project-specific terms
        "Unknown word: Kimera",
        "Unknown word: echoform",
        "Unknown word: duckdb",
        "Unknown word: ndarray"
    ],
    
    # Critical issues that should fail tests
    "critical_patterns": [
        "SyntaxError",
        "ImportError",
        "ModuleNotFoundError",
        "IndentationError"
    ]
}

# Paths
BASE_DIR = Path.cwd()
SRC_DIR = BASE_DIR / "src"
VAULT_DIR = BASE_DIR / "vault"
TEST_DIR = BASE_DIR
CI_FILE = BASE_DIR / ".github" / "workflows" / "ci.yml"

# Test categories
TEST_CATEGORIES = {
    "import": "Import and module loading tests",
    "functionality": "Core functionality tests", 
    "system": "System-level tests",
    "integration": "Integration and end-to-end tests",
    "ci": "CI configuration and workflow tests"
}

# Expected modules and their key components
EXPECTED_MODULES = {
    "kimera.identity": ["Identity", "create_geoid_identity"],
    "kimera.storage": ["LatticeStorage"],
    "kimera.reactor_mp": ["adaptive_tau", "decay_factor"],
    "vault.core.vault": ["Vault"]
}

def get_test_config():
    """Get the test configuration."""
    return TEST_CONFIG

def get_required_files():
    """Get list of required files."""
    return TEST_CONFIG["required_structure"]["files"]

def get_required_directories():
    """Get list of required directories."""
    return TEST_CONFIG["required_structure"]["directories"]

def should_ignore_issue(issue_text):
    """Check if an issue should be ignored."""
    for pattern in TEST_CONFIG["ignore_patterns"]:
        if pattern in issue_text:
            return True
    return False

def is_critical_issue(issue_text):
    """Check if an issue is critical."""
    for pattern in TEST_CONFIG["critical_patterns"]:
        if pattern in issue_text:
            return True
    return False