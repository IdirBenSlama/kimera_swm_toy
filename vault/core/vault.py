"""
Basic vault implementation for Kimera SWM.
"""

from typing import Dict, Any, Optional
from pathlib import Path
import json

class Vault:
    """Basic vault for storing and retrieving data."""
    
    def __init__(self, vault_path: str = "vault_data"):
        self.vault_path = Path(vault_path)
        self.vault_path.mkdir(exist_ok=True)
    
    def store(self, key: str, data: Any) -> bool:
        """Store data in the vault."""
        try:
            file_path = self.vault_path / f"{key}.json"
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
    
    def retrieve(self, key: str) -> Optional[Any]:
        """Retrieve data from the vault."""
        try:
            file_path = self.vault_path / f"{key}.json"
            if file_path.exists():
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception:
            return None
    
    def snapshot(self) -> Dict[str, Any]:
        """Create a snapshot of all vault data."""
        snapshot = {}
        for file_path in self.vault_path.glob("*.json"):
            key = file_path.stem
            data = self.retrieve(key)
            if data is not None:
                snapshot[key] = data
        return snapshot