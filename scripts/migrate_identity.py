#!/usr/bin/env python3
"""
Migration script for unified identity system
Migrates EchoForm data to unified Identity table with verification logging
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from kimera.storage import LatticeStorage
from kimera.identity import create_geoid_identity
from kimera.echoform import EchoForm


def add_identity_schema(storage: LatticeStorage) -> None:
    """Add the unified identity schema to the database"""
    print("🔧 Adding identity schema...")
    
    # Create the unified identities table
    storage.conn.execute("""
        CREATE TABLE IF NOT EXISTS identities (
            id TEXT PRIMARY KEY,
            identity_type TEXT NOT NULL,
            raw TEXT NOT NULL,
            terms TEXT,
            tags TEXT,
            relationships TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for performance
    storage.conn.execute("CREATE INDEX IF NOT EXISTS idx_identities_type ON identities(identity_type)")
    storage.conn.execute("CREATE INDEX IF NOT EXISTS idx_identities_created ON identities(created_at)")
    
    print("✅ Identity schema added")


def migrate_echoforms_to_identities(storage: LatticeStorage) -> List[Dict[str, Any]]:
    """
    Migrate existing EchoForm data to unified Identity table
    Returns migration log for verification
    """
    print("🔄 Migrating EchoForms to unified Identity table...")
    
    migration_log = []
    
    # Check if dual-write mode is enabled
    dual_write = os.environ.get("KIMERA_ID_DUAL_WRITE", "0") == "1"
    if dual_write:
        print("⚠️  Dual-write mode enabled - new identities will be stored in both tables")
    
    try:
        # Fetch all existing EchoForms
        echoforms = storage.conn.execute("SELECT * FROM echoforms").fetchall()
        
        for row in echoforms:
            anchor = row[0]
            raw = row[1]
            terms = row[2] if len(row) > 2 else ""
            lang = row[3] if len(row) > 3 else "en"
            created_at = row[4] if len(row) > 4 else datetime.utcnow()
            
            # Create corresponding Identity
            identity = create_geoid_identity(
                raw, 
                tags=[f"lang:{lang}", "migrated_from_echoform"]
            )
            
            # Store in identities table
            storage.conn.execute("""
                INSERT OR REPLACE INTO identities 
                (id, identity_type, raw, terms, tags, relationships, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                identity.id,
                identity.identity_type,
                identity.raw,
                json.dumps(identity.terms) if identity.terms else "[]",
                json.dumps(identity.tags) if identity.tags else "[]",
                json.dumps(identity.relationships) if identity.relationships else "[]",
                created_at,
                datetime.utcnow()
            ))
            
            # Log migration
            log_entry = {
                "echoform_anchor": anchor,
                "identity_id": identity.id,
                "migration_timestamp": datetime.utcnow().isoformat(),
                "raw_content": raw,
                "original_lang": lang
            }
            migration_log.append(log_entry)
            
        storage.conn.commit()
        print(f"✅ Migrated {len(migration_log)} EchoForms to Identity table")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        storage.conn.rollback()
        raise
    
    return migration_log


def verify_migration(storage: LatticeStorage, migration_log: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verify the migration was successful"""
    print("🔍 Verifying migration...")
    
    verification = {
        "total_migrated": len(migration_log),
        "verification_timestamp": datetime.utcnow().isoformat(),
        "data_integrity_checks": {}
    }
    
    # Check that all migrated identities exist
    missing_identities = []
    for log_entry in migration_log:
        identity_id = log_entry["identity_id"]
        result = storage.conn.execute(
            "SELECT id FROM identities WHERE id = ?", 
            (identity_id,)
        ).fetchone()
        
        if not result:
            missing_identities.append(identity_id)
    
    verification["data_integrity_checks"]["missing_identities"] = missing_identities
    verification["data_integrity_checks"]["all_identities_present"] = len(missing_identities) == 0
    
    # Check identity type distribution
    type_counts = storage.conn.execute("""
        SELECT identity_type, COUNT(*) 
        FROM identities 
        GROUP BY identity_type
    """).fetchall()
    
    verification["data_integrity_checks"]["identity_type_distribution"] = dict(type_counts)
    
    if len(missing_identities) == 0:
        print("✅ Migration verification passed")
    else:
        print(f"❌ Migration verification failed: {len(missing_identities)} missing identities")
    
    return verification


def create_sample_scar_identities(storage: LatticeStorage) -> List[str]:
    """Create some sample scar identities for testing"""
    print("🧪 Creating sample scar identities...")
    
    from kimera.identity import create_scar_identity
    
    scar_ids = []
    
    # Create a few sample scars
    scar1 = create_scar_identity(
        "Contradiction between concepts A and B",
        relationships=[
            {"target_id": "concept_a", "type": "contradicts", "strength": 0.8},
            {"target_id": "concept_b", "type": "contradicts", "strength": 0.8}
        ],
        tags=["contradiction", "sample"]
    )
    
    scar2 = create_scar_identity(
        "Reference to external source",
        relationships=[
            {"target_id": "external_source", "type": "references", "strength": 0.6}
        ],
        tags=["reference", "sample"]
    )
    
    # Store them
    storage.store_identity(scar1)
    storage.store_identity(scar2)
    
    scar_ids.extend([scar1.id, scar2.id])
    
    print(f"✅ Created {len(scar_ids)} sample scar identities")
    return scar_ids


def main():
    """Run the complete migration process"""
    print("🚀 Starting Identity Migration Process")
    
    # Use environment variable for database path, default to temporary
    db_path = os.environ.get("KIMERA_DB_PATH", ":memory:")
    
    try:
        storage = LatticeStorage(db_path)
        
        # Step 1: Add identity schema
        add_identity_schema(storage)
        
        # Step 2: Migrate existing data
        migration_log = migrate_echoforms_to_identities(storage)
        
        # Step 3: Verify migration
        verification = verify_migration(storage, migration_log)
        
        # Step 4: Create sample scar identities
        scar_ids = create_sample_scar_identities(storage)
        
        # Step 5: Generate final report
        report = {
            "migration_log": migration_log,
            "verification": verification,
            "sample_scar_ids": scar_ids,
            "migration_completed": datetime.utcnow().isoformat()
        }
        
        # Save report if not in-memory database
        if db_path != ":memory:":
            report_path = f"migration_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Migration report saved to {report_path}")
        
        print("🎉 Migration completed successfully!")
        storage.close()
        
        return report
        
    except Exception as e:
        print(f"💥 Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    main()