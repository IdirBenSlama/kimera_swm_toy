from kimera.geoid import init_geoid
from kimera.reactor import reactor_cycle, reactor_cycle_batched
from kimera import resonance as _res
from kimera import reactor as _reactor


def test_reactor_cycle_runs():
    g1 = init_geoid("The sky is blue", "en", ["default"])
    g2 = init_geoid("Quantum entanglement defies locality", "en", ["default"])
    reactor_cycle([g1, g2])
    assert any(g.scars for g in (g1, g2))


def test_reactor_batch_stats():
    """Guarantee scar creation by temporarily raising THRESH in both modules."""
    # Save original values
    orig_res_thresh = _res.THRESH
    orig_reactor_thresh = _reactor.THRESH
    
    # Patch both locations
    _res.THRESH = 0.95
    _reactor.THRESH = 0.95  # reactor imported a copy – patch too

    geoids = []
    for i in range(200):
        geoids.append(init_geoid(f"Cats purr softly {i}", "en", ["default"]))
        geoids.append(init_geoid(f"Quantum entanglement defies locality {i}", "en", ["default"]))

    stats = reactor_cycle_batched(geoids, chunk=100, verbose=False)

    # Restore original values
    _res.THRESH = orig_res_thresh
    _reactor.THRESH = orig_reactor_thresh

    assert stats["geoids"] == 400
    assert stats["latency_ms"] > 0
    assert stats["new_scars"] >= 1
