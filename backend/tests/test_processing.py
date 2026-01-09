import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_and_process():
    # upload small fake file
    files = {"file": ("sample.mp4", b"\x00\x00\x00\x18ftypmp42", "video/mp4")}
    r = client.post('/api/videos/demo-experiment', files=files)
    assert r.status_code == 201
    j = r.json()
    vid = j['id']

    # poll for status (timeout 10s)
    deadline = time.time() + 10
    status = None
    while time.time() < deadline:
        r2 = client.get(f'/api/videos/{vid}')
        assert r2.status_code == 200
        data = r2.json()
        status = data.get('status')
        if status == 'processed' or status == 'failed':
            break
        time.sleep(0.5)

    assert status == 'processed'
