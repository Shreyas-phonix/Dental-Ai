from fastapi.testclient import TestClient

from backend.app import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_missing_file_rejected():
    response = client.post("/api/v1/predict")
    assert response.status_code == 422


def test_invalid_file_rejected(tmp_path):
    bad_file = tmp_path / "not_an_image.txt"
    bad_file.write_text("hello world")
    response = client.post(
        "/api/v1/predict",
        files={"file": ("not_an_image.txt", bad_file.read_bytes(), "text/plain")},
    )
    assert response.status_code == 400
