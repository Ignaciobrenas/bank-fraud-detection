def test_feature_engineering_loads():
    from src.fraud_detection.features import build_gold
    assert callable(build_gold.run_build_gold)
