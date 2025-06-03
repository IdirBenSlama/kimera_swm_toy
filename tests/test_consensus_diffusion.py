import numpy as np

from src.kimera.next_evolution import (
    Geoid,
    GeoidSubstrate,
    ConsensusEngine,
    VerboseDiffusionNarrator,
    Booklaw,
    ComplianceGrid,
)


def unit_vector(dim=32, seed=0):
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim)
    return vec / np.linalg.norm(vec)


def test_consensus_generation():
    substrate = GeoidSubstrate(dimension=32)
    g1 = Geoid(unit_vector(seed=1), symbols={"a"})
    g2 = Geoid(unit_vector(seed=2), symbols={"b"})
    g3 = Geoid(unit_vector(seed=3), symbols={"c"})
    for g in (g1, g2, g3):
        substrate.add_geoid(g)

    # No booklaw rules for test
    engine = ConsensusEngine(substrate, compliance=ComplianceGrid(Booklaw()))
    consensus = engine.generate_consensus([g1.id, g2.id, g3.id])

    # Consensus geoid must be in substrate
    assert consensus.id in substrate.geoids
    # Essence vector unit norm (tolerance)
    assert np.isclose(np.linalg.norm(consensus.core.essence), 1.0, atol=1e-6)


def test_verbose_narrative():
    substrate = GeoidSubstrate(dimension=16)
    g = Geoid(unit_vector(dim=16, seed=4), symbols={"x"})
    substrate.add_geoid(g)

    narrator = VerboseDiffusionNarrator(substrate)
    text = narrator.diffuse([g.id], verbosity=1)

    assert isinstance(text, str)
    assert g.id[:8] in text  # Geoid id should appear in narrative
