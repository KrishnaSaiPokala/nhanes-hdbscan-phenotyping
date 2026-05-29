def test_package_imports():
    import nhanes_hdbscan

    assert nhanes_hdbscan.__version__ == "0.1.0"


def test_core_modules_import():
    from nhanes_hdbscan import config, reporting, results, visualization

    assert config.PROJECT_SHORT_NAME
    assert results.REQUIRED_KEYS
    assert visualization is not None
    assert reporting is not None
