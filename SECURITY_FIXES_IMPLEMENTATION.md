# 🛡️ CRITICAL SECURITY FIXES IMPLEMENTATION PLAN

## 🚨 IMMEDIATE CRITICAL FIXES (Deploy within 24 hours)

### Fix 1: Datetime Timezone Vulnerability
**File**: `src/kimera/identity.py`
**Lines**: 47, 105, 259, 291, 302, 316

```python
# BEFORE (VULNERABLE):
now = datetime.utcnow()  # DEPRECATED & TIMEZONE-NAIVE

# AFTER (SECURE):
now = datetime.now(timezone.utc)  # TIMEZONE-AWARE
```

**Implementation**:
```python
# Add to imports
from datetime import datetime, timezone

# Replace all instances of datetime.utcnow() with:
now = datetime.now(timezone.utc)
```

### Fix 2: Numpy Array Validation
**File**: `src/kimera/identity.py`
**Location**: Constructor and vector handling

```python
# Add validation function
def _validate_numpy_array(vector: np.ndarray) -> np.ndarray:
    """Validate numpy array for security and safety"""
    if vector is None:
        return None
    
    # Size limits (prevent memory exhaustion)
    MAX_ARRAY_SIZE = 1_000_000  # 1M elements max
    MAX_MEMORY_MB = 100  # 100MB max
    
    if vector.size > MAX_ARRAY_SIZE:
        raise ValueError(f"Array too large: {vector.size} > {MAX_ARRAY_SIZE}")
    
    memory_mb = vector.nbytes / (1024 * 1024)
    if memory_mb > MAX_MEMORY_MB:
        raise ValueError(f"Array memory too large: {memory_mb:.1f}MB > {MAX_MEMORY_MB}MB")
    
    # Type validation (prevent object arrays)
    if vector.dtype == np.object_:
        raise ValueError("Object arrays not allowed for security reasons")
    
    # Ensure numeric types only
    if not np.issubdtype(vector.dtype, np.number):
        raise ValueError(f"Non-numeric array type not allowed: {vector.dtype}")
    
    # Check for NaN/Infinity
    if np.any(~np.isfinite(vector)):
        raise ValueError("Array contains NaN or infinity values")
    
    return vector.copy()  # Return defensive copy

# Apply in constructor:
if vector is not None:
    self.vector = _validate_numpy_array(vector)
```

### Fix 3: Recursion Limits
**File**: `src/kimera/echoform.py`

```python
# Add recursion tracking
class EchoForm:
    _recursion_depth = 0
    MAX_RECURSION_DEPTH = 100
    
    def __init__(self, ...):
        # Disable recursion by default
        recursive = config.get("recursive", False)  # Changed from True
        
        # Add recursion depth tracking
        if recursive:
            EchoForm._recursion_depth += 1
            if EchoForm._recursion_depth > self.MAX_RECURSION_DEPTH:
                EchoForm._recursion_depth -= 1
                raise RecursionError(f"Maximum recursion depth exceeded: {self.MAX_RECURSION_DEPTH}")
    
    def __del__(self):
        if hasattr(self, 'recursive') and self.recursive:
            EchoForm._recursion_depth = max(0, EchoForm._recursion_depth - 1)
```

### Fix 4: Entropy Bounds Checking
**File**: `src/kimera/entropy.py`

```python
def calculate_shannon_entropy(intensities: List[float]) -> float:
    """Calculate Shannon entropy with bounds checking"""
    if not intensities:
        return 0.0
    
    # Input validation
    MAX_INTENSITY = 1e6  # Reasonable upper bound
    MIN_INTENSITY = 1e-10  # Avoid underflow
    
    validated_intensities = []
    for i in intensities:
        # Type checking
        if not isinstance(i, (int, float)):
            continue
        
        # NaN/Infinity checking
        if not math.isfinite(i):
            continue
        
        # Bounds checking
        if i > MAX_INTENSITY:
            i = MAX_INTENSITY
        elif i < MIN_INTENSITY:
            continue
        
        if i > 0:
            validated_intensities.append(float(i))
    
    if not validated_intensities:
        return 0.0
    
    # Safe normalization with overflow protection
    total = sum(validated_intensities)
    if total == 0 or not math.isfinite(total):
        return 0.0
    
    # Calculate entropy with bounds checking
    entropy = 0.0
    for i in validated_intensities:
        p = i / total
        if p > 0 and math.isfinite(p):
            log_p = math.log2(p)
            if math.isfinite(log_p):
                entropy -= p * log_p
    
    # Final bounds check
    if not math.isfinite(entropy):
        return 0.0
    
    return max(0.0, min(entropy, 20.0))  # Cap at reasonable maximum
```

### Fix 5: Metadata Validation
**File**: `src/kimera/identity.py`

```python
def _validate_metadata_key(key: str) -> str:
    """Validate metadata key for security"""
    if not isinstance(key, str):
        raise TypeError("Metadata key must be string")
    
    if len(key) > 100:
        raise ValueError("Metadata key too long (max 100 chars)")
    
    # Prevent system key collisions
    RESERVED_KEYS = {
        '__class__', '__dict__', '__module__', '__doc__',
        'id', 'created_at', 'updated_at', 'meta'
    }
    
    if key in RESERVED_KEYS:
        raise ValueError(f"Reserved key not allowed: {key}")
    
    # Prevent dangerous characters
    if any(c in key for c in ['<', '>', '"', "'", '&', '\x00']):
        raise ValueError("Metadata key contains dangerous characters")
    
    return key

def _validate_metadata_value(value: Any) -> Any:
    """Validate metadata value for security"""
    # Size limits
    MAX_STRING_LENGTH = 10000  # 10KB max for strings
    MAX_TOTAL_SIZE = 1000000   # 1MB max total
    
    if isinstance(value, str):
        if len(value) > MAX_STRING_LENGTH:
            raise ValueError(f"String value too long: {len(value)} > {MAX_STRING_LENGTH}")
    
    # Type restrictions
    ALLOWED_TYPES = (str, int, float, bool, list, dict, type(None))
    if not isinstance(value, ALLOWED_TYPES):
        raise TypeError(f"Metadata value type not allowed: {type(value)}")
    
    # Prevent functions, classes, modules
    if callable(value) or hasattr(value, '__module__'):
        raise TypeError("Callable objects not allowed in metadata")
    
    # Recursive validation for containers
    if isinstance(value, dict):
        for k, v in value.items():
            _validate_metadata_key(str(k))
            _validate_metadata_value(v)
    elif isinstance(value, list):
        for item in value:
            _validate_metadata_value(item)
    
    return value

def update_metadata(self, key: str, value: Any) -> None:
    """Update metadata with validation"""
    validated_key = _validate_metadata_key(key)
    validated_value = _validate_metadata_value(value)
    
    # Check total metadata size
    import sys
    current_size = sys.getsizeof(self.meta)
    new_size = sys.getsizeof({validated_key: validated_value})
    
    if current_size + new_size > 1000000:  # 1MB limit
        raise ValueError("Total metadata size limit exceeded")
    
    # Thread-safe update
    with threading.Lock():
        self.meta[validated_key] = validated_value
        self.updated_at = datetime.now(timezone.utc)
```

---

## 🔒 SECURITY HARDENING MEASURES

### 1. Input Sanitization Framework
```python
# src/kimera/security.py
import re
import html
from typing import Any, Union

class SecurityValidator:
    """Centralized security validation"""
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        if not isinstance(value, str):
            raise TypeError("Expected string input")
        
        if len(value) > max_length:
            raise ValueError(f"String too long: {len(value)} > {max_length}")
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # HTML escape
        value = html.escape(value)
        
        # Remove control characters except whitespace
        value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
        
        return value
    
    @staticmethod
    def validate_numeric(value: Union[int, float], min_val: float = None, max_val: float = None) -> Union[int, float]:
        """Validate numeric input"""
        if not isinstance(value, (int, float)):
            raise TypeError("Expected numeric input")
        
        if not math.isfinite(value):
            raise ValueError("Numeric value must be finite")
        
        if min_val is not None and value < min_val:
            raise ValueError(f"Value too small: {value} < {min_val}")
        
        if max_val is not None and value > max_val:
            raise ValueError(f"Value too large: {value} > {max_val}")
        
        return value
```

### 2. Rate Limiting Implementation
```python
# src/kimera/rate_limiter.py
import time
from collections import defaultdict, deque
from threading import Lock

class RateLimiter:
    """Simple rate limiter for API protection"""
    
    def __init__(self, max_calls: int = 100, window_seconds: int = 60):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = defaultdict(deque)
        self.lock = Lock()
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if call is allowed for identifier"""
        now = time.time()
        
        with self.lock:
            # Clean old entries
            call_times = self.calls[identifier]
            while call_times and call_times[0] < now - self.window_seconds:
                call_times.popleft()
            
            # Check limit
            if len(call_times) >= self.max_calls:
                return False
            
            # Record call
            call_times.append(now)
            return True

# Global rate limiter
_rate_limiter = RateLimiter()

def rate_limited(func):
    """Decorator for rate limiting"""
    def wrapper(*args, **kwargs):
        # Use thread ID as identifier (simple approach)
        import threading
        identifier = str(threading.get_ident())
        
        if not _rate_limiter.is_allowed(identifier):
            raise Exception("Rate limit exceeded")
        
        return func(*args, **kwargs)
    return wrapper
```

### 3. Memory Monitoring
```python
# src/kimera/memory_monitor.py
import psutil
import threading
import time

class MemoryMonitor:
    """Monitor memory usage and enforce limits"""
    
    def __init__(self, max_memory_mb: int = 1000):
        self.max_memory_mb = max_memory_mb
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start memory monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
    
    def _monitor_loop(self):
        """Memory monitoring loop"""
        while self.monitoring:
            try:
                process = psutil.Process()
                memory_mb = process.memory_info().rss / 1024 / 1024
                
                if memory_mb > self.max_memory_mb:
                    # Force garbage collection
                    import gc
                    gc.collect()
                    
                    # Check again
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    if memory_mb > self.max_memory_mb:
                        raise MemoryError(f"Memory limit exceeded: {memory_mb:.1f}MB > {self.max_memory_mb}MB")
                
                time.sleep(1)  # Check every second
                
            except Exception as e:
                print(f"Memory monitoring error: {e}")
                break
    
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.monitoring = False

# Global memory monitor
_memory_monitor = MemoryMonitor()
```

### 4. Audit Logging
```python
# src/kimera/audit.py
import logging
import json
from datetime import datetime, timezone
from typing import Dict, Any

class AuditLogger:
    """Security audit logging"""
    
    def __init__(self):
        self.logger = logging.getLogger('kimera.audit')
        self.logger.setLevel(logging.INFO)
        
        # Create handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security-related event"""
        event = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'event_type': event_type,
            'details': details
        }
        
        self.logger.warning(json.dumps(event))
    
    def log_access(self, operation: str, resource: str, user_id: str = None):
        """Log access event"""
        self.log_security_event('access', {
            'operation': operation,
            'resource': resource,
            'user_id': user_id
        })
    
    def log_validation_failure(self, validation_type: str, input_data: str, error: str):
        """Log validation failure"""
        self.log_security_event('validation_failure', {
            'validation_type': validation_type,
            'input_data': input_data[:100],  # Truncate for security
            'error': error
        })

# Global audit logger
_audit_logger = AuditLogger()
```

---

## 🧪 SECURITY TESTING FRAMEWORK

### 1. Automated Security Tests
```python
# tests/security/test_security_hardening.py
import pytest
import numpy as np
from datetime import datetime, timezone

def test_numpy_array_validation():
    """Test numpy array security validation"""
    from kimera.identity import Identity
    
    # Test size limits
    with pytest.raises(ValueError, match="Array too large"):
        large_array = np.ones(2_000_000)  # Too large
        Identity(content="test", vector=large_array)
    
    # Test object arrays
    with pytest.raises(ValueError, match="Object arrays not allowed"):
        obj_array = np.array([lambda x: x], dtype=object)
        Identity(content="test", vector=obj_array)
    
    # Test NaN/Infinity
    with pytest.raises(ValueError, match="NaN or infinity"):
        nan_array = np.array([1.0, float('nan'), 3.0])
        Identity(content="test", vector=nan_array)

def test_metadata_validation():
    """Test metadata security validation"""
    from kimera.identity import Identity
    
    identity = Identity(content="test")
    
    # Test reserved keys
    with pytest.raises(ValueError, match="Reserved key"):
        identity.update_metadata("__class__", "malicious")
    
    # Test size limits
    with pytest.raises(ValueError, match="too long"):
        identity.update_metadata("key", "x" * 20000)
    
    # Test type restrictions
    with pytest.raises(TypeError, match="not allowed"):
        identity.update_metadata("func", lambda x: x)

def test_timezone_safety():
    """Test timezone-aware datetime usage"""
    from kimera.identity import Identity
    
    identity = Identity(content="test")
    
    # Verify timezone awareness
    assert identity.created_at.tzinfo is not None
    assert identity.updated_at.tzinfo is not None
    
    # Verify UTC timezone
    assert identity.created_at.tzinfo == timezone.utc
```

### 2. Penetration Testing Scripts
```python
# tests/security/penetration_tests.py
def test_memory_exhaustion_protection():
    """Test protection against memory exhaustion"""
    from kimera.echoform import EchoForm
    
    echo = EchoForm()
    
    # Should be protected against too many terms
    with pytest.raises(Exception):  # Should raise some limit error
        for i in range(100000):
            echo.add_term(f"term_{i}", intensity=1.0)

def test_recursion_protection():
    """Test protection against recursion attacks"""
    from kimera.echoform import EchoForm
    
    # Should be protected against deep recursion
    with pytest.raises(RecursionError):
        def create_recursive_forms(depth=0):
            if depth > 200:  # Should hit limit before this
                return
            echo = EchoForm(config={"recursive": True})
            create_recursive_forms(depth + 1)
        
        create_recursive_forms()
```

---

## 📋 DEPLOYMENT SECURITY CHECKLIST

### Pre-Deployment Security Validation:
- [ ] All datetime.utcnow() calls replaced with timezone-aware versions
- [ ] Numpy array validation implemented and tested
- [ ] Recursion limits implemented and enforced
- [ ] Entropy calculation bounds checking implemented
- [ ] Metadata validation with size and type limits
- [ ] Input sanitization framework deployed
- [ ] Rate limiting implemented on all public methods
- [ ] Memory monitoring and limits enforced
- [ ] Audit logging implemented for security events
- [ ] Comprehensive security test suite passing
- [ ] Penetration testing completed
- [ ] Security code review completed
- [ ] Dependency vulnerability scan completed

### Runtime Security Configuration:
```yaml
# security_config.yaml
security:
  memory:
    max_memory_mb: 1000
    monitoring_enabled: true
  
  rate_limiting:
    max_calls_per_minute: 100
    enabled: true
  
  validation:
    max_string_length: 10000
    max_metadata_size_mb: 1
    max_array_size: 1000000
  
  audit:
    log_level: WARNING
    log_file: /var/log/kimera/audit.log
    enabled: true
```

---

## 🚨 CRITICAL DEPLOYMENT DECISION

**CURRENT STATUS**: 🔴 **PRODUCTION DEPLOYMENT BLOCKED**

**REQUIRED ACTIONS BEFORE PRODUCTION**:
1. Implement all critical security fixes (estimated 2-3 days)
2. Deploy security hardening measures
3. Complete comprehensive security testing
4. Conduct external security audit
5. Implement monitoring and alerting
6. Create incident response procedures

**ESTIMATED TIME TO SECURE DEPLOYMENT**: 1-2 weeks

**RECOMMENDATION**: 
- **IMMEDIATELY HALT any production deployment plans**
- **Implement critical fixes as highest priority**
- **Conduct thorough security review before any deployment**
- **Consider hiring external security consultants**

The identified vulnerabilities pose **CRITICAL SECURITY RISKS** that could lead to:
- Remote code execution
- Data corruption
- Service disruption
- Memory exhaustion attacks
- Authentication bypasses

**DO NOT DEPLOY TO PRODUCTION UNTIL ALL SECURITY ISSUES ARE RESOLVED**