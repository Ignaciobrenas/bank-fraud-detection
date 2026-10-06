from fastapi.testclient import TestClient
from src.fraud_detection.api.serve import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"

def test_predict_endpoint_validation_error():
    # Sending missing parameters should result in 422 Unprocessable Entity
    response = client.post("/predict", json={"transaction_id": "tx-123"})
    assert response.status_code == 422
