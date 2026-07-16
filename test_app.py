import json
from app import app


def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_health():
    c = client()
    resp = c.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_create_and_get_task():
    c = client()
    resp = c.post("/tasks", json={"title": "Write CI/CD pipeline"})
    assert resp.status_code == 201
    task = resp.get_json()
    assert task["title"] == "Write CI/CD pipeline"
    assert task["done"] is False

    resp2 = c.get(f"/tasks/{task['id']}")
    assert resp2.status_code == 200


def test_create_task_missing_title():
    c = client()
    resp = c.post("/tasks", json={})
    assert resp.status_code == 400


def test_complete_and_delete_task():
    c = client()
    resp = c.post("/tasks", json={"title": "Temp task"})
    task_id = resp.get_json()["id"]

    resp2 = c.put(f"/tasks/{task_id}/complete")
    assert resp2.status_code == 200
    assert resp2.get_json()["done"] is True

    resp3 = c.delete(f"/tasks/{task_id}")
    assert resp3.status_code == 204


def test_get_nonexistent_task():
    c = client()
    resp = c.get("/tasks/does-not-exist")
    assert resp.status_code == 404
