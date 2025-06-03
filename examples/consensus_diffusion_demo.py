import numpy as np

from src.kimera.next_evolution import (
    Geoid,
    GeoidSubstrate,
    ComplianceGrid,
    Booklaw,
    AuditLedger,
    ConsensusEngine,
    VerboseDiffusionNarrator,
)


def random_vector(dim=64):
    vec = np.random.randn(dim)
    return vec / np.linalg.norm(vec)


def main():
    # Initialise substrate and booklaw (empty rule-set for demo)
    substrate = GeoidSubstrate(dimension=64)
    booklaw = Booklaw()
    compliance = ComplianceGrid(booklaw)
    ledger = AuditLedger()

    # Create a few demo geoids
    g1 = Geoid(random_vector(), modality="language", symbols={"alpha"})
    g2 = Geoid(random_vector(), modality="language", symbols={"beta"})
    g3 = Geoid(random_vector(), modality="language", symbols={"gamma"})

    for g in (g1, g2, g3):
        substrate.add_geoid(g)

    # ---------------- Consensus ----------------
    engine = ConsensusEngine(substrate, compliance=compliance, audit_ledger=ledger)
    consensus = engine.generate_consensus([g1.id, g2.id, g3.id])

    print("Created consensus geoid:", consensus.id)

    # ---------------- Diffusion Narrative ----------------
    narrator = VerboseDiffusionNarrator(substrate)
    story = narrator.diffuse([g1.id, g2.id, g3.id, consensus.id], verbosity=2)

    print("\n=== VERBOSE DIFFUSION NARRATIVE ===\n")
    print(story)


if __name__ == "__main__":
    main()
