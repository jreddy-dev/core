import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_upload_with_consent_and_encryption(tmp_path):
    # set encryption env
    from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    os.environ['ENCRYPT_VIDEOS'] = '1'
    os.environ['ENCRYPTION_KEY'] = key.decode()

    files = {"file": ("sample.mp4", b"\x00\x00\x00\x18ftypmp42", "video/mp4"), 'consent': 'true'}
    r = client.post('/api/videos/demo-experiment', files=files)
    assert r.status_code == 201
    vid = r.json()['id']

    r2 = client.get(f'/api/videos/{vid}')
    assert r2.status_code == 200
    data = r2.json()
    assert data['consent_for_training'] is True
    assert data['encrypted'] is True

    # cleanup env
    del os.environ['ENCRYPT_VIDEOS']
    del os.environ['ENCRYPTION_KEY']
