from kimera.geoid import init_geoid


def test_init_geoid():
    g = init_geoid("Hello world", "en", ["default"])
    assert g.raw == "Hello world"
    assert g.lang_axis == "en"
    assert g.sem_vec.shape[0] == 384 or g.sem_vec.shape[0] == 512
