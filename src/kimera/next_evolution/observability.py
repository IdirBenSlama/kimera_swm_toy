"""
Observability & Manipulation Layer (Operator Interface)

Provides live monitoring, injection hooks, and vault forensics for system diagnosis and research.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import json

class Watchtower:
    """
    Live dashboard for monitoring geoids, scars, and contradiction flows.
    """
    def __init__(self, substrate, scar_vault, contradiction_reactor):
        self.substrate = substrate
        self.scar_vault = scar_vault
        self.contradiction_reactor = contradiction_reactor

    def snapshot(self) -> Dict[str, Any]:
        """Return a snapshot of the current system state."""
        return {
            'timestamp': datetime.now().isoformat(),
            'substrate_stats': self.substrate.get_substrate_stats(),
            'scar_vault_stats': self.scar_vault.get_stats(),
            'active_contradictions': [
                {
                    'id': e.id,
                    'geoids': (e.geoid_a, e.geoid_b),
                    'intensity': e.intensity,
                    'resolved': e.resolved
                }
                for e in self.contradiction_reactor.active_contradictions.values()
            ]
        }

    def print_snapshot(self):
        snap = self.snapshot()
        print(json.dumps(snap, indent=2))

    def live_monitor(self, interval: float = 2.0, steps: int = 10):
        """Print live system state at intervals (for demonstration)."""
        import time
        for _ in range(steps):
            self.print_snapshot()
            time.sleep(interval)

    def inject_contradiction(self, geoid_a_id: str, geoid_b_id: str, intensity: float, notes: str = "manual"):
        return self.contradiction_reactor.inject_contradiction(geoid_a_id, geoid_b_id, intensity, notes)

    def inject_scar(self, geoid_ids: List[str], contradiction_event_id: str, intensity: float):
        return self.scar_vault.create_scar(geoid_ids, contradiction_event_id, intensity)

class VaultForensics:
    """
    Forensic tools for replay, mutation tracing, and echoform mapping.
    """
    def __init__(self, audit_ledger, substrate, scar_vault):
        self.audit_ledger = audit_ledger
        self.substrate = substrate
        self.scar_vault = scar_vault

    def replay_events(self, event_type: Optional[str] = None):
        """Replay events for forensic analysis."""
        for entry in self.audit_ledger.get_events(event_type):
            print(f"[{entry.timestamp}] {entry.event_type} {entry.event_id}: {entry.details}")

    def trace_geoid_mutations(self, geoid_id: str):
        """Trace all mutations for a given geoid."""
        for entry in self.audit_ledger.get_events("mutation"):
            if entry.details.get('geoid_id') == geoid_id:
                print(f"[{entry.timestamp}] Mutation: {entry.details}")

    def echoform_map(self, geoid_id: str):
        """Map all scars and echoforms for a geoid."""
        scars = self.scar_vault.scars_for_geoid(geoid_id)
        print(f"Geoid {geoid_id} scars:")
        for scar in scars:
            print(f"  Scar {scar.id} | Echo strength: {scar.echo_strength:.3f} | Reactivations: {scar.reactivation_count}")
