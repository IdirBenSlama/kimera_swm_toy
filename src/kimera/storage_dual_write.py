"""
Storage layer enhancement for dual-write functionality.
This module extends the base storage to support dual-write mode for safe migration.
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

from .storage import LatticeStorage, storage_timer
from .identity import Identity
from .echoform import EchoForm

# Import observability hooks
try:
    from .observability import track_dual_write_operation, log_dual_write_event
    OBSERVABILITY_AVAILABLE = True
except ImportError:
    # Fallback if prometheus_client is not available
    OBSERVABILITY_AVAILABLE = False
    def track_dual_write_operation(func):
        return func
    def log_dual_write_event(identity_id, operation, status):
        pass


class DualWriteStorage(LatticeStorage):
    """
    Extended storage class with dual-write capability for migration.
    
    When dual-write is enabled, all identity operations are written to both
    the new identity table and a legacy format table for backward compatibility.
    """
    
    def __init__(self, db_path: str = "kimera_lattice.db"):
        super().__init__(db_path)
        
        # Check if dual-write is enabled via environment variable
        self.dual_write_enabled = os.getenv('KIMERA_ID_DUAL_WRITE', '0') == '1'
        
        if self.dual_write_enabled:
            self._init_legacy_schema()
            print(f"🔄 Dual-write mode ENABLED for storage at {db_path}")
        else:
            print(f"📝 Single-write mode (dual-write disabled) for storage at {db_path}")
    
    def _init_legacy_schema(self):
        """Initialize legacy schema for dual-write mode"""
        with self._lock:
            with storage_timer("legacy_schema_init"):
                # Legacy geoids table (for backward compatibility)
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS legacy_geoids (
                        gid TEXT PRIMARY KEY,
                        raw TEXT NOT NULL,
                        echo TEXT,
                        lang_axis TEXT,
                        tags JSON,
                        weight DOUBLE,
                        meta JSON,
                        created_at DOUBLE,
                        updated_at DOUBLE
                    );
                """)
                
                # Legacy scars table (for backward compatibility)
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS legacy_scars (
                        id TEXT PRIMARY KEY,
                        weight DOUBLE,
                        related_ids JSON,
                        meta JSON,
                        created_at DOUBLE,
                        updated_at DOUBLE
                    );
                """)
                
                # Dual-write audit log
                self._conn.execute("""
                    CREATE SEQUENCE IF NOT EXISTS dual_write_log_seq;
                """)
                
                self._conn.execute("""
                    CREATE TABLE IF NOT EXISTS dual_write_log (
                        log_id INTEGER PRIMARY KEY DEFAULT nextval('dual_write_log_seq'),
                        timestamp DOUBLE NOT NULL,
                        identity_id TEXT NOT NULL,
                        operation TEXT NOT NULL,
                        status TEXT NOT NULL,
                        details JSON
                    );
                """)
    
    @track_dual_write_operation
    def store_identity(self, identity: Identity):
        """Store identity with dual-write support"""
        # Always store in the new identity table
        super().store_identity(identity)
        
        # If dual-write is enabled, also store in legacy format
        if self.dual_write_enabled:
            try:
                self._store_legacy_format(identity)
                self._log_dual_write(identity.id, "store", "success")
                
                if OBSERVABILITY_AVAILABLE:
                    log_dual_write_event(identity.id, "store", "success")
                    
            except Exception as e:
                self._log_dual_write(identity.id, "store", "failed", {"error": str(e)})
                
                if OBSERVABILITY_AVAILABLE:
                    log_dual_write_event(identity.id, "store", "failed")
                
                # Re-raise to maintain consistency
                raise
    
    def _store_legacy_format(self, identity: Identity):
        """Store identity in legacy format tables"""
        with self._lock:
            now = time.time()
            
            if identity.identity_type == "geoid":
                # Store in legacy geoids table
                with storage_timer("store_legacy_geoid"):
                    self._conn.execute("""
                        INSERT OR REPLACE INTO legacy_geoids 
                        (gid, raw, echo, lang_axis, tags, weight, meta, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, 
                            COALESCE((SELECT created_at FROM legacy_geoids WHERE gid = ?), ?),
                            ?)
                    """, (
                        identity.id, identity.raw, identity.echo, identity.lang_axis,
                        json.dumps(identity.tags), identity.weight, json.dumps(identity.meta),
                        identity.id, now, now
                    ))
                    
            elif identity.identity_type == "scar":
                # Store in legacy scars table
                with storage_timer("store_legacy_scar"):
                    self._conn.execute("""
                        INSERT OR REPLACE INTO legacy_scars 
                        (id, weight, related_ids, meta, created_at, updated_at)
                        VALUES (?, ?, ?, ?, 
                            COALESCE((SELECT created_at FROM legacy_scars WHERE id = ?), ?),
                            ?)
                    """, (
                        identity.id, identity.weight, json.dumps(identity.related_ids),
                        json.dumps(identity.meta), identity.id, now, now
                    ))
    
    def _log_dual_write(self, identity_id: str, operation: str, status: str, details: Optional[Dict] = None):
        """Log dual-write operation for audit trail"""
        with self._lock:
            self._conn.execute("""
                INSERT INTO dual_write_log (timestamp, identity_id, operation, status, details)
                VALUES (?, ?, ?, ?, ?)
            """, (
                time.time(), identity_id, operation, status,
                json.dumps(details) if details else None
            ))
    
    def verify_dual_write_consistency(self, identity_id: str) -> Dict[str, Any]:
        """Verify consistency between new and legacy storage"""
        if not self.dual_write_enabled:
            return {"error": "Dual-write not enabled"}
        
        # Fetch from new storage
        new_identity = self.fetch_identity(identity_id)
        if not new_identity:
            return {"error": "Identity not found in new storage"}
        
        # Fetch from legacy storage
        legacy_data = None
        if new_identity.identity_type == "geoid":
            result = self._conn.execute(
                "SELECT * FROM legacy_geoids WHERE gid = ?", (identity_id,)
            ).fetchone()
            if result:
                legacy_data = {
                    "gid": result[0],
                    "raw": result[1],
                    "echo": result[2],
                    "lang_axis": result[3],
                    "tags": json.loads(result[4]) if result[4] else [],
                    "weight": result[5],
                    "meta": json.loads(result[6]) if result[6] else {},
                    "created_at": result[7],
                    "updated_at": result[8]
                }
        elif new_identity.identity_type == "scar":
            result = self._conn.execute(
                "SELECT * FROM legacy_scars WHERE id = ?", (identity_id,)
            ).fetchone()
            if result:
                legacy_data = {
                    "id": result[0],
                    "weight": result[1],
                    "related_ids": json.loads(result[2]) if result[2] else [],
                    "meta": json.loads(result[3]) if result[3] else {},
                    "created_at": result[4],
                    "updated_at": result[5]
                }
        
        if not legacy_data:
            return {"error": "Identity not found in legacy storage"}
        
        # Compare key fields
        discrepancies = []
        
        if new_identity.identity_type == "geoid":
            if new_identity.raw != legacy_data.get("raw"):
                discrepancies.append(f"raw: '{new_identity.raw}' != '{legacy_data.get('raw')}'")
            if new_identity.echo != legacy_data.get("echo"):
                discrepancies.append(f"echo: '{new_identity.echo}' != '{legacy_data.get('echo')}'")
            if new_identity.lang_axis != legacy_data.get("lang_axis"):
                discrepancies.append(f"lang_axis: '{new_identity.lang_axis}' != '{legacy_data.get('lang_axis')}'")
            if new_identity.tags != legacy_data.get("tags", []):
                discrepancies.append(f"tags: {new_identity.tags} != {legacy_data.get('tags', [])}")
        
        if abs(new_identity.weight - legacy_data.get("weight", 1.0)) > 0.0001:
            discrepancies.append(f"weight: {new_identity.weight} != {legacy_data.get('weight', 1.0)}")
        
        return {
            "identity_id": identity_id,
            "identity_type": new_identity.identity_type,
            "consistent": len(discrepancies) == 0,
            "discrepancies": discrepancies,
            "new_data": new_identity.to_dict(),
            "legacy_data": legacy_data
        }
    
    def get_dual_write_stats(self) -> Dict[str, Any]:
        """Get statistics about dual-write operations"""
        if not self.dual_write_enabled:
            return {"error": "Dual-write not enabled"}
        
        with storage_timer("get_dual_write_stats"):
            # Count operations
            total_ops = self._conn.execute(
                "SELECT COUNT(*) FROM dual_write_log"
            ).fetchone()[0]
            
            success_ops = self._conn.execute(
                "SELECT COUNT(*) FROM dual_write_log WHERE status = 'success'"
            ).fetchone()[0]
            
            failed_ops = self._conn.execute(
                "SELECT COUNT(*) FROM dual_write_log WHERE status = 'failed'"
            ).fetchone()[0]
            
            # Count entities
            new_identities = self.get_identity_count()
            legacy_geoids = self._conn.execute(
                "SELECT COUNT(*) FROM legacy_geoids"
            ).fetchone()[0]
            legacy_scars = self._conn.execute(
                "SELECT COUNT(*) FROM legacy_scars"
            ).fetchone()[0]
            
            # Get recent operations
            recent_ops = self._conn.execute("""
                SELECT timestamp, identity_id, operation, status, details
                FROM dual_write_log
                ORDER BY timestamp DESC
                LIMIT 10
            """).fetchall()
            
            return {
                "dual_write_enabled": True,
                "total_operations": total_ops,
                "successful_operations": success_ops,
                "failed_operations": failed_ops,
                "success_rate": (success_ops / total_ops * 100) if total_ops > 0 else 0,
                "new_identities_count": new_identities,
                "legacy_geoids_count": legacy_geoids,
                "legacy_scars_count": legacy_scars,
                "total_legacy_count": legacy_geoids + legacy_scars,
                "recent_operations": [
                    {
                        "timestamp": op[0],
                        "identity_id": op[1],
                        "operation": op[2],
                        "status": op[3],
                        "details": json.loads(op[4]) if op[4] else None
                    }
                    for op in recent_ops
                ]
            }
    
    def cleanup_legacy_tables(self):
        """Remove legacy tables after successful migration"""
        if self.dual_write_enabled:
            raise RuntimeError("Cannot cleanup legacy tables while dual-write is enabled")
        
        with self._lock:
            self._conn.execute("DROP TABLE IF EXISTS legacy_geoids")
            self._conn.execute("DROP TABLE IF EXISTS legacy_scars")
            self._conn.execute("DROP TABLE IF EXISTS dual_write_log")
            print("🧹 Legacy tables cleaned up successfully")


# Factory function to get storage with dual-write support
def get_dual_write_storage(db_path: str = "kimera_lattice.db") -> DualWriteStorage:
    """Get storage instance with dual-write support"""
    return DualWriteStorage(db_path)