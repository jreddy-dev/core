from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_synth_and_save_protocol():
    # upload small fake file
    files = {"file": ("sample.mp4", b"\x00\x00\x00\x18ftypmp42", "video/mp4")}
    r = client.post('/api/videos/demo-experiment', files=files)
    assert r.status_code == 201
    vid = r.json()['id']

    # call synthesize
    r2 = client.post(f'/api/videos/{vid}/synthesize')
    assert r2.status_code == 200
    md = r2.json().get('protocol_markdown')
    assert md is not None

    # save to experiment
    r3 = client.post('/api/protocols/experiment/demo-experiment', json={'content_markdown': md, 'generated_by_video_id': vid})
    assert r3.status_code == 200
    pid = r3.json()['id']
    assert pid is not None

    # list protocols
    r4 = client.get('/api/protocols/experiment/demo-experiment')
    assert r4.status_code == 200
    assert any(p['id'] == pid for p in r4.json())
