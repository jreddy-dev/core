from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get('/health')
    assert r.status_code == 200


def test_upload_missing_file():
    r = client.post('/api/videos/demo-experiment')
    assert r.status_code == 422
