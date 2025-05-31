from kimera.geoid import init_geoid


def test_init_geoid():
    g = init_geoid("Hello world", "en", ["default"])
    assert g.raw == "Hello world"
    assert g.echo == "Hello world"  # Should be trimmed version of raw
    assert g.lang_axis == "en"
    assert g.sem_vec.shape[0] == 384 or g.sem_vec.shape[0] == 512


def test_echo_trimming():
    """Test that echo field properly trims whitespace"""
    g = init_geoid("  Hello world  ", "en", ["default"])
    assert g.raw == "  Hello world  "
    assert g.echo == "Hello world"  # Should be trimmed


def test_stable_gid_from_echo():
    """Test that gid is stable and based on echo"""
    g1 = init_geoid("Hello world", "en", ["default"])
    g2 = init_geoid("  Hello world  ", "en", ["default"])  # Same echo after trim
    g3 = init_geoid("Hello world!", "en", ["default"])     # Different echo
    
    assert g1.gid == g2.gid  # Same echo should give same gid
    assert g1.gid != g3.gid  # Different echo should give different gid
