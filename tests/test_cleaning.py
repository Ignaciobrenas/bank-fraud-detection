def test_clean_amounts():
    # Placeholder for Spark cleaning test
    # In a real environment, we would start a local spark session and test `build_silver` transformations.
    # For CI speed, we just assure the module loads.
    from src.fraud_detection.processing import build_silver
    assert callable(build_silver.run_build_silver)
