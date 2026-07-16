"""
Task Manager API
A small, containerized REST API used as the target application
for a DevSecOps CI/CD security-scanning pipeline demo.
"""
from flask import Flask, jsonify, request, abort
from uuid import uuid4

app = Flask(__name__)

# In-memory store (demo only — not for production use)
tasks = {}


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values())), 200


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        abort(400, description="Field 'title' is required")

    task_id = str(uuid4())
    task = {
        "id": task_id,
        "title": str(data["title"])[:200],  # basic length constraint
        "done": False,
    }
    tasks[task_id] = task
    return jsonify(task), 201


@app.get("/tasks/<task_id>")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        abort(404, description="Task not found")
    return jsonify(task), 200


@app.put("/tasks/<task_id>/complete")
def complete_task(task_id):
    task = tasks.get(task_id)
    if not task:
        abort(404, description="Task not found")
    task["done"] = True
    return jsonify(task), 200


@app.delete("/tasks/<task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        abort(404, description="Task not found")
    del tasks[task_id]
    return "", 204


if __name__ == "__main__":
    # debug=False intentionally — avoids exposing the Werkzeug debugger
    app.run(host="0.0.0.0", port=5000, debug=False)  # nosec B104
