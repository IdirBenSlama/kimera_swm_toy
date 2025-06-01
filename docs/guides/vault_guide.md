# Kimera Vault Guide

## Overview

The Kimera Vault provides a persistent key-value store for managing secrets, configuration data, and other sensitive information within the Kimera ecosystem.

## Basic Usage

### Creating a Vault
```python
from vault.core.vault import Vault

# Initialize vault with database path
vault = Vault("/path/to/vault.db")
```

### Storing Data
```python
# Store simple values
vault.set("api_key", "your-secret-api-key")
vault.set("model_config", {"temperature": 0.7, "max_tokens": 1000})
vault.set("user_preferences", {"theme": "dark", "notifications": True})
```

### Retrieving Data
```python
# Get stored values
api_key = vault.get("api_key")
config = vault.get("model_config")

# Handle missing keys
user_id = vault.get("user_id", default="anonymous")
```

### Checking Existence
```python
# Check if key exists
if vault.has("api_key"):
    print("API key is configured")
else:
    print("API key not found")
```

## Advanced Features

### Snapshots
```python
# Create a snapshot of all vault data
snapshot = vault.snapshot()
print(f"Vault contains {len(snapshot)} items")

# Iterate through all stored data
for key, value in snapshot.items():
    print(f"{key}: {type(value).__name__}")
```

### Data Types
```python
# Vault supports various data types
vault.set("string_value", "hello world")
vault.set("integer_value", 42)
vault.set("float_value", 3.14159)
vault.set("boolean_value", True)
vault.set("list_value", [1, 2, 3, "four"])
vault.set("dict_value", {"nested": {"data": "structure"}})
```

### Bulk Operations
```python
# Store multiple values at once
config_data = {
    "database_url": "sqlite:///app.db",
    "debug_mode": False,
    "max_connections": 100,
    "timeout_seconds": 30
}

for key, value in config_data.items():
    vault.set(key, value)
```

## Integration with Kimera

### Configuration Management
```python
# Store Kimera configuration
vault.set("kimera_config", {
    "default_tau_days": 14.0,
    "entropy_scaling_factor": 0.1,
    "storage_path": "/data/kimera.db",
    "cache_enabled": True
})

# Retrieve and use configuration
config = vault.get("kimera_config")
storage = LatticeStorage(
    config["storage_path"], 
    default_tau_days=config["default_tau_days"]
)
```

### API Key Management
```python
# Securely store API keys
vault.set("openai_api_key", "sk-...")
vault.set("anthropic_api_key", "ant-...")

# Use in applications
import os
api_key = vault.get("openai_api_key")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
```

### User Session Data
```python
# Store user session information
vault.set("current_session", {
    "user_id": "user_123",
    "session_start": "2024-12-19T10:30:00Z",
    "active_workspace": "project_alpha",
    "preferences": {
        "auto_save": True,
        "show_debug": False
    }
})
```

## Security Considerations

### Data Sensitivity
```python
# Mark sensitive data (for future encryption support)
vault.set("password", "secret123")  # Note: Currently stored as plaintext
vault.set("private_key", "-----BEGIN PRIVATE KEY-----...")

# Consider using environment variables for highly sensitive data
import os
vault.set("db_password", os.getenv("DB_PASSWORD", ""))
```

### Access Patterns
```python
# Implement access logging (custom wrapper)
class LoggedVault:
    def __init__(self, vault_path):
        self.vault = Vault(vault_path)
        self.access_log = []
    
    def get(self, key, default=None):
        self.access_log.append(f"READ: {key}")
        return self.vault.get(key, default)
    
    def set(self, key, value):
        self.access_log.append(f"WRITE: {key}")
        return self.vault.set(key, value)
```

## Backup and Recovery

### Creating Backups
```python
import json
import datetime

# Create a backup of vault data
snapshot = vault.snapshot()
backup_data = {
    "timestamp": datetime.datetime.now().isoformat(),
    "data": snapshot
}

# Save backup to file
backup_filename = f"vault_backup_{datetime.date.today()}.json"
with open(backup_filename, "w") as f:
    json.dump(backup_data, f, indent=2)
```

### Restoring from Backup
```python
# Restore vault from backup
with open("vault_backup_2024-12-19.json", "r") as f:
    backup_data = json.load(f)

# Clear existing data (optional)
# vault.clear()  # If this method exists

# Restore data
for key, value in backup_data["data"].items():
    vault.set(key, value)
```

## Performance Optimization

### Batch Operations
```python
# Minimize database operations
def bulk_update(vault, updates):
    """Update multiple vault entries efficiently."""
    for key, value in updates.items():
        vault.set(key, value)
    # Consider implementing transaction support in future versions
```

### Caching Frequently Accessed Data
```python
class CachedVault:
    def __init__(self, vault_path, cache_size=100):
        self.vault = Vault(vault_path)
        self.cache = {}
        self.cache_size = cache_size
    
    def get(self, key, default=None):
        if key in self.cache:
            return self.cache[key]
        
        value = self.vault.get(key, default)
        if len(self.cache) < self.cache_size:
            self.cache[key] = value
        
        return value
    
    def set(self, key, value):
        self.vault.set(key, value)
        self.cache[key] = value  # Update cache
```

## Testing and Development

### Test Vault Setup
```python
import tempfile
import os

def create_test_vault():
    """Create a temporary vault for testing."""
    temp_dir = tempfile.mkdtemp()
    vault_path = os.path.join(temp_dir, "test_vault.db")
    return Vault(vault_path)

# Use in tests
def test_vault_operations():
    vault = create_test_vault()
    
    # Test basic operations
    vault.set("test_key", "test_value")
    assert vault.get("test_key") == "test_value"
    assert vault.has("test_key") == True
    assert vault.has("nonexistent") == False
```

### Development Utilities
```python
def vault_info(vault):
    """Display vault information for debugging."""
    snapshot = vault.snapshot()
    
    print(f"Vault contains {len(snapshot)} items:")
    for key, value in snapshot.items():
        value_type = type(value).__name__
        value_preview = str(value)[:50]
        if len(str(value)) > 50:
            value_preview += "..."
        print(f"  {key}: {value_type} = {value_preview}")
```

## Migration and Compatibility

### Vault Format Evolution
```python
def migrate_vault_format(old_vault_path, new_vault_path):
    """Migrate vault data to new format (future use)."""
    old_vault = Vault(old_vault_path)
    new_vault = Vault(new_vault_path)
    
    # Copy all data
    snapshot = old_vault.snapshot()
    for key, value in snapshot.items():
        new_vault.set(key, value)
    
    print(f"Migrated {len(snapshot)} items")
```

## Best Practices

1. **Use descriptive keys** with consistent naming conventions
2. **Store configuration data** rather than hardcoding values
3. **Implement backup strategies** for important vault data
4. **Consider data sensitivity** when storing secrets
5. **Use snapshots** for debugging and data inspection
6. **Test vault operations** in development environments
7. **Monitor vault size** for performance considerations

## Limitations and Future Enhancements

### Current Limitations
- **No encryption**: Data is stored as plaintext
- **No access control**: All data is accessible to vault users
- **No transaction support**: Operations are not atomic
- **No compression**: Large data may impact performance

### Planned Enhancements
- **Encryption support**: Encrypt sensitive data at rest
- **Access control**: Role-based access to vault keys
- **Transaction support**: Atomic operations for data consistency
- **Compression**: Automatic compression for large values
- **Replication**: Multi-vault synchronization

## Troubleshooting

### Common Issues

**Database Lock Errors**:
```python
# Ensure proper vault cleanup
try:
    vault = Vault("vault.db")
    # ... operations ...
finally:
    # Close vault connection if method exists
    pass
```

**Data Type Issues**:
```python
# Ensure data is JSON-serializable
import json

def safe_vault_set(vault, key, value):
    try:
        json.dumps(value)  # Test serialization
        vault.set(key, value)
    except TypeError:
        print(f"Value for key '{key}' is not JSON-serializable")
```

**Performance Issues**:
- Use bulk operations when possible
- Implement caching for frequently accessed data
- Consider vault size and cleanup old data
- Monitor database file size and performance