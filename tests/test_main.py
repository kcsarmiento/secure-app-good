import pytest
from app.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_greet_valid(client):
    r = client.post("/greet", json={"name": "Alice"})
    assert r.status_code == 200
    assert "Hello, Alice!" in r.get_json()["message"]

def test_greet_missing_name(client):
    r = client.post("/greet", json={})
    assert r.status_code == 400

def test_greet_xss_attack(client):
    r = client.post("/greet", json={"name": "<script>alert(1)</script>"})
    assert r.status_code == 400
