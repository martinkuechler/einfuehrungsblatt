# tests/test_api.py
import pytest
from fastapi.testclient import TestClient

# WICHTIG: Pfad anpassen, falls deine Datei anders heißt/liegt.
# In deinem Projekt heißt sie "backend/apipy.py" und enthält "app = FastAPI()".
from backend.api import app

client = TestClient(app)


def cleanup():
    """Räumt die DB rein über die API auf (keine direkten DB-Zugriffe)."""
    r = client.get("/api/items")
    assert r.status_code == 200
    for it in r.json():
        client.delete(f"/api/items/{it['id']}")


def test_ping_pong():
    cleanup()
    r = client.get("/api/ping")
    assert r.status_code == 200


    r2 = client.post("/api/pong")
    assert r2.status_code == 200
    assert r2.text == '""'#fast api returned leere strings anscheinend so und nicht als ==""


def test_create_then_list_contains():
    cleanup()
    payload = {"id": 1, "title": "test", "content": "some content"}

    r_create = client.post("/api/items", json=payload)
    # dein POST gibt aktuell 200 + "" zurück
    assert r_create.status_code == 200
    assert r_create.text == '""'

    r_list = client.get("/api/items")
    assert r_list.status_code == 200
    lst = r_list.json()
    assert len(lst) == 1
    it = lst[0]
    assert it["id"] == 1
    assert it["title"] == "test"
    assert it["content"] == "some content"
    assert "created_at" in it


def test_duplicate_rejection():
    cleanup()
    p = {"id": 5, "title": "a", "content": "b"}
    client.post("/api/items", json=p)

    r_dup = client.post("/api/items", json=p)
    # deine API antwortet mit Text (200) statt 409/400 – wir prüfen den Text
    assert r_dup.status_code == 409



def test_delete_roundtrip():
    cleanup()
    client.post("/api/items", json={"id": 1, "title": "x", "content": "y"})
    client.post("/api/items", json={"id": 2, "title": "z", "content": "w"})

    r_del = client.delete("/api/items/1")
    assert r_del.status_code == 200
    r_list = client.get("/api/items")
    assert r_list.status_code == 200
    ids = {it["id"] for it in r_list.json()}
    assert ids == {2}


def test_get_by_id():
    cleanup()
    client.post("/api/items", json={"id": 10, "title": "foo", "content": "bar"})
    r = client.get("/api/items/10")

    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 10
    assert data["title"] == "foo"
    assert data["content"] == "bar"
    assert "created_at" in data

