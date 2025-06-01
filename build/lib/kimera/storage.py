"""
Persistent lattice storage using DuckDB.
Very first cut - only what the current tests need.Now with observability and entropy tracking."""

import time
import threading
import json
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import contextmanager
from collections import Counter
from uuid import uuid4
from datetime import datetime

try:
    import duckdb
except ImportError:
    raise ImportError("DuckDB is required for persistent storage. Install with: pip install duckdb")

from .echoform import EchoForm
from .identity import Identity
# Import observability hooks
try:
    from .observability import track_entropy, storage_operations_timer, update_identity_gauges, log_entropy_event
    OBSERVABILITY_AVAILABLE = True
except ImportError:
    # Fallback if prometheus_client is not available
    OBSERVABILITY_AVAILABLE = False
    def track_entropy(func):
        return func
# Global metrics collection
_lattice_stats = Counter()

@contextmanager
def storage_timer(metric: str):
    """Context manager to time storage operations and collect metrics"""
    start = time.perf_counter()
    try:
        yield
    finally:
        dt = time.perf_counter() - start
        _lattice_stats[metric] += dt
        _lattice_stats[f"{metric}_count"] += 1

def get_storage_metrics() -> Dict[str, float]:
    """Get current storage metrics"""
    return dict(_lattice_stats)

def reset_storage_metrics():
    """Reset storage metrics"""
    global _lattice_stats
    _lattice_stats = Counter()

# Global storage instance
_storage_instance = None
_storage_lock = threading.RLock()

class LatticeStorage:
    """DuckDB-based persistent storage for EchoForms"""
    
    def __init__(self, db_path: str = "kimera_lattice.db"):
        self.db_path = Path(db_path)
        
        # Handle existing file that might not be a valid DuckDB
        if self.db_path.exists():
            try:
                # Test if it's a valid DuckDB file
                test_conn = duckdb.connect(str(self.db_path))
                test_conn.close()
            except duckdb.IOException:
                # Not a valid DuckDB file - remove it
                self.db_path.unlink()
        
        self._conn = duckdb.connect(str(self.db_path), read_only=False)
        self._lock = threading.RLock()
        self._init_schema()
    
    def _init_schema(self):
        """Initialize the database schema"""
        with self._lock:
            with storage_timer("schema_init"):
                # EchoForms table
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS echoforms (
                        anchor TEXT PRIMARY KEY,
                        blob JSON,
                        created_at DOUBLE,
                        updated_at DOUBLE,
                        domain TEXT,
                        phase TEXT,
                        intensity_sum DOUBLE
                    );
                """)
                
                # Identities table for unified identity model
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS identities (
                        id TEXT PRIMARY KEY,
                        identity_type TEXT NOT NULL,
                        data JSON NOT NULL,
                        created_at DOUBLE NOT NULL,
                        updated_at DOUBLE NOT NULL,
                        lang_axis TEXT,
                        entropy_score DOUBLE
                    );
                """)
                
                # Create indexes for performance
                self._conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_echoforms_updated_at 
                    ON echoforms(updated_at DESC);
                """)
                
                self._conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_echoforms_domain 
                    ON echoforms(domain);
                """)
                
                self._conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_identities_updated_at 
                    ON identities(updated_at DESC);
                """)
                
                self._conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_identities_type 
                    ON identities(identity_type);
                """)
                
                self._conn.execute("""
                    CREATE INDEX IF NOT EXISTS idx_identities_entropy 
                    ON identities(entropy_score DESC);
                """)
    
    def store_form(self, form: EchoForm):
        """Store or update an EchoForm"""
        with self._lock:
            blob = form.flatten()
            now = time.time()
            
            with storage_timer("store_form"):
                self._conn.execute("""
                    INSERT OR REPLACE INTO echoforms 
                    (anchor, blob, created_at, updated_at, domain, phase, intensity_sum)
                    VALUES (?, ?, 
                        COALESCE((SELECT created_at FROM echoforms WHERE anchor = ?), ?),
                        ?, ?, ?, ?)
                """, (
                    form.anchor, blob, form.anchor, now, now,
                    form.domain, form.phase, form.intensity_sum()
                ))
    
    def fetch_form(self, anchor: str) -> Optional[EchoForm]:
        """Fetch an EchoForm by anchor"""
        with storage_timer("fetch_form"):
            result = self._conn.execute(
                "SELECT blob FROM echoforms WHERE anchor = ?", (anchor,)
            ).fetchone()
        
        if result:
            return EchoForm.reinflate(result[0])
        return None
    
    def update_form(self, form: EchoForm):
        """Update an existing form (alias for store_form)"""
        self.store_form(form)
    
    def list_forms(self, limit: int = 10, domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """List recent forms with metadata"""
        query = """
            SELECT anchor, created_at, updated_at, domain, phase, intensity_sum
            FROM echoforms
        """
        params = []
        
        if domain:
            query += " WHERE domain = ?"
            params.append(domain)
        
        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        
        with storage_timer("list_forms"):
            rows = self._conn.execute(query, params).fetchall()
        
        return [
            {
                "anchor": row[0],
                "created_at": row[1],
                "updated_at": row[2],
                "domain": row[3],
                "phase": row[4],
                "intensity_sum": row[5]
            }
            for row in rows
        ]
    
    def get_form_count(self, domain: Optional[str] = None) -> int:
        """Get count of stored forms"""
        with storage_timer("get_form_count"):
            if domain:
                result = self._conn.execute(
                    "SELECT COUNT(*) FROM echoforms WHERE domain = ?", (domain,)
                ).fetchone()
            else:
                result = self._conn.execute("SELECT COUNT(*) FROM echoforms").fetchone()
        
        return result[0] if result else 0
    
    def prune_old_forms(self, older_than_seconds: float = None, older_than_days: float = None):
        """Remove forms older than specified time
        
        Args:
            older_than_seconds: Time threshold in seconds (preferred)
            older_than_days: Time threshold in days (legacy compatibility)
        """
        if older_than_days is not None:
            cutoff_seconds = older_than_days * 24 * 3600
        elif older_than_seconds is not None:
            cutoff_seconds = older_than_seconds
        else:
            cutoff_seconds = 30.0 * 24 * 3600  # Default 30 days
            
        cutoff = time.time() - cutoff_seconds
        with self._lock:
            with storage_timer("prune_old_forms"):
                cursor = self._conn.execute(
                    "DELETE FROM echoforms WHERE created_at < ?", (cutoff,)
                )
                deleted = cursor.rowcount  # Grab before commit
                self._conn.commit()
                return deleted
    
    def apply_time_decay(self, tau_days: float = 14.0):
        """Apply exponential time decay to all forms"""
        tau_seconds = tau_days * 24 * 3600
        now = time.time()
        
        with self._lock:
            with storage_timer("apply_time_decay"):
                # Get all forms
                rows = self._conn.execute(
                    "SELECT anchor, blob, created_at FROM echoforms"
                ).fetchall()
                
                for anchor, blob, created_at in rows:
                    form = EchoForm.reinflate(blob)
                    age_seconds = now - created_at
                    
                    # Apply decay to all terms
                    import math
                    decay_factor = math.exp(-age_seconds / tau_seconds)
                    
                    for term in form.terms:
                        if 'intensity' in term:
                            term['intensity'] *= decay_factor
                    
                    # Update the form
                    self.store_form(form)
    
    def close(self):
        """Close the database connection"""
        with self._lock:
            if hasattr(self, '_conn') and self._conn:
                self._conn.close()
                self._conn = None

    # Identity storage methods
    
    @track_entropy
    def store_identity(self, identity: Identity):
        """Store or update an Identity with entropy tracking"""
        with self._lock:
            import json
            data_json = json.dumps(identity.to_dict())
            now = time.time()
            entropy_score = identity.entropy()
            effective_tau = identity.effective_tau()
            
            # Log entropy event for observability
            if OBSERVABILITY_AVAILABLE:
                log_entropy_event(identity.id, entropy_score, effective_tau, "store")
            
            with storage_timer("store_identity"):
                self._conn.execute("""
                    INSERT OR REPLACE INTO identities 
                    (id, identity_type, data, created_at, updated_at, lang_axis, entropy_score)
                    VALUES (?, ?, ?, 
                        COALESCE((SELECT created_at FROM identities WHERE id = ?), ?),
                        ?, ?, ?)
                """, (
                    identity.id, identity.identity_type, data_json,
                    identity.id, now, now, identity.lang_axis, entropy_score
                ))
                
            # Update gauge metrics
            if OBSERVABILITY_AVAILABLE:
                update_identity_gauges(self)
    
    def fetch_identity(self, identity_id: str) -> Optional[Identity]:
        """Fetch an Identity by ID"""
        with storage_timer("fetch_identity"):
            result = self._conn.execute(
                "SELECT data FROM identities WHERE id = ?", (identity_id,)
            ).fetchone()
        
        if result:
            import json
            data = json.loads(result[0])
            return Identity.from_dict(data)
        return None
    
    def list_identities(self, limit: int = 10, identity_type: Optional[str] = None, 
                       lang_axis: Optional[str] = None) -> List[Dict[str, Any]]:
        """List identities with metadata"""
        query = """
            SELECT id, identity_type, created_at, updated_at, lang_axis, entropy_score
            FROM identities
        """
        params = []
        conditions = []
        
        if identity_type:
            conditions.append("identity_type = ?")
            params.append(identity_type)
        
        if lang_axis:
            conditions.append("lang_axis = ?")
            params.append(lang_axis)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)
        
        with storage_timer("list_identities"):
            rows = self._conn.execute(query, params).fetchall()
        
        return [
            {
                "id": row[0],
                "identity_type": row[1],
                "created_at": row[2],
                "updated_at": row[3],
                "lang_axis": row[4],
                "entropy_score": row[5]
            }
            for row in rows
        ]
    
    def get_identity_count(self, identity_type: Optional[str] = None) -> int:
        """Get count of stored identities"""
        with storage_timer("get_identity_count"):
            if identity_type:
                result = self._conn.execute(
                    "SELECT COUNT(*) FROM identities WHERE identity_type = ?", (identity_type,)
                ).fetchone()
            else:
                result = self._conn.execute("SELECT COUNT(*) FROM identities").fetchone()
        
        return result[0] if result else 0
    
    def find_identities_by_entropy(self, min_entropy: float = 0.0, 
                                  max_entropy: float = float('inf'), 
                                  limit: int = 10) -> List[Identity]:
        """Find identities within entropy range"""
        with storage_timer("find_identities_by_entropy"):
            rows = self._conn.execute("""
                SELECT data FROM identities 
                WHERE entropy_score >= ? AND entropy_score <= ?
                ORDER BY entropy_score DESC 
                LIMIT ?
            """, (min_entropy, max_entropy, limit)).fetchall()
        
        identities = []
        for row in rows:
            import json
            data = json.loads(row[0])
            identities.append(Identity.from_dict(data))
        
        return identities
    
    def apply_identity_decay(self, base_tau_days: float = 14.0):
        """Apply entropy-adjusted time decay to all identities"""
        now = time.time()
        
        with self._lock:
            with storage_timer("apply_identity_decay"):
                # Get all identities
                rows = self._conn.execute(
                    "SELECT id, data, created_at FROM identities"
                ).fetchall()
                
                for identity_id, data_json, created_at in rows:
                    import json
                    identity = Identity.from_dict(json.loads(data_json))
                    
                    # Calculate effective tau based on entropy
                    effective_tau = identity.effective_tau(base_tau_days * 24 * 3600)
                    age_seconds = now - created_at
                    
                    # Apply decay factor
                    import math
                    decay_factor = math.exp(-age_seconds / effective_tau)
                    
                    # Apply decay to identity weight and related metadata
                    identity.weight *= decay_factor
                    
                    # If identity has terms in meta, decay their intensities
                    if "terms" in identity.meta:
                        for term in identity.meta["terms"]:
                            if "intensity" in term:
                                term["intensity"] *= decay_factor
                    
                    # Update the identity
                    self.store_identity(identity)

    # ─── Compatibility Stubs ──────────────────────────────────────────────────

    def store_geoid(self, geoid_obj):
        """
        Legacy alias: accept a Geoid-type object and store it as an Identity.
        """
        # Convert geoid to identity if needed
        if hasattr(geoid_obj, 'to_dict'):
            # It's already an Identity-like object
            identity = geoid_obj
        else:
            # Try to convert from legacy geoid format
            from .identity import Identity
            identity = Identity(content=str(geoid_obj))
        
        self.store_identity(identity)

    def store_scar(self, scar_obj):
        """
        Legacy alias: accept a SCAR-type object and store it as an Identity.
        """
        # Convert scar to identity if needed
        if hasattr(scar_obj, 'to_dict'):
            # It's already an Identity-like object
            identity = scar_obj
        else:
            # Try to convert from legacy scar format
            from .identity import Identity
            identity = Identity.create_scar(content=str(scar_obj))
        
        self.store_identity(identity)

    def store_echo_form(self, echo_form_obj: EchoForm):
        """
        Legacy alias: if tests call store_echo_form, convert echoform to a Geoid identity.
        """
        import json
        from uuid import uuid4
        from datetime import datetime
        
        # Serialize the EchoForm into its raw field
        raw_json = echo_form_obj.to_dict() if hasattr(echo_form_obj, "to_dict") else {}
        
        # Generate a "geoid" identity with that JSON blob as raw
        from .identity import Identity
        new_id = f"geoid_{uuid4().hex}"
        identity = Identity(
            id=new_id,
            identity_type="geoid",
            raw=json.dumps(raw_json),
            echo="",
            lang_axis="en",
            tags=[],
            vector=None,
            weight=1.0,
            related_ids=[],
            meta={"source": "echo_form", "anchor": echo_form_obj.anchor},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.store_identity(identity)

    def fetch_geoid(self, gid: str) -> Optional[Identity]:
        """
        Alias for fetch_identity, since a geoid is just an identity of type 'geoid'.
        """
        return self.fetch_identity(gid)

    def get_identity(self, identity_id: str) -> Optional[Identity]:
        """Alias for fetch_identity for backward compatibility"""
        return self.fetch_identity(identity_id)

    def search_identities(self, query: str, limit: int = 10) -> List[Identity]:
        """Search for identities by content"""
        try:
            cursor = self._conn.cursor()
            # Search in both raw and echo fields
            cursor.execute("""
                SELECT * FROM identities 
                WHERE raw LIKE ? OR echo LIKE ?
                ORDER BY updated_at DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))
            
            results = []
            for row in cursor.fetchall():
                identity = self._row_to_identity(row)
                if identity:
                    results.append(identity)
            
            return results
        except Exception as e:
            print(f"Error searching identities: {e}")
            return []

    def close(self):
        """Close the database connection"""
        if hasattr(self, '_conn') and self._conn:
            self._conn.close()


def get_storage(db_path: str = "kimera_lattice.db") -> LatticeStorage:
    """Get or create the global storage instance"""
    global _storage_instance
    
    with _storage_lock:
        if _storage_instance is None:
            _storage_instance = LatticeStorage(db_path)
        return _storage_instance


def close_storage():
    """Close the global storage instance"""
    global _storage_instance
    
    with _storage_lock:
        if _storage_instance is not None:
            _storage_instance.close()
            _storage_instance = None


# Legacy functions for backward compatibility
def store_form(anchor: str, echo_blob: str):
    """Store an EchoForm JSON blob (legacy interface)"""
    form = EchoForm.reinflate(echo_blob)
    get_storage().store_form(form)


def fetch_form(anchor: str) -> Optional[str]:
    """Fetch an EchoForm JSON blob (legacy interface)"""
    form = get_storage().fetch_form(anchor)
    return form.flatten() if form else None


def fetch_recent(n: int = 10) -> List[tuple]:
    """Fetch recent forms (legacy interface)"""
    forms_list = get_storage().list_forms(limit=n)
    result = []
    
    for form_meta in forms_list:
        form = get_storage().fetch_form(form_meta["anchor"])
        if form:
            result.append((
                form_meta["anchor"],
                form.flatten(),
                form_meta["created_at"]
            ))
    
    return result


def delete_older_than(sec: float):
    """Delete forms older than specified seconds (legacy interface)"""
    get_storage().prune_old_forms(sec)