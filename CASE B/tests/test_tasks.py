"""
Tests for the Task CRUD endpoints.
"""


def test_create_task(client):
    """POST /tasks should create a new task."""
    response = client.post("/tasks", json={
        "title": "Test Task",
        "description": "A test task",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "A test task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_task_minimal(client):
    """POST /tasks with only required fields."""
    response = client.post("/tasks", json={"title": "Minimal Task"})
    assert response.status_code == 201
    assert response.json()["title"] == "Minimal Task"


def test_create_task_empty_title_fails(client):
    """POST /tasks with empty title should fail validation."""
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks_empty(client):
    """GET /tasks should return empty list initially."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks(client):
    """GET /tasks should return created tasks."""
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_tasks_filter_completed(client):
    """GET /tasks?completed=true should filter tasks."""
    client.post("/tasks", json={"title": "Incomplete"})
    res = client.post("/tasks", json={"title": "Done", "completed": True})
    task_id = res.json()["id"]
    client.put(f"/tasks/{task_id}", json={"completed": True})

    response = client.get("/tasks?completed=true")
    assert response.status_code == 200
    tasks = response.json()
    assert all(t["completed"] for t in tasks)


def test_get_task(client):
    """GET /tasks/{id} should return a specific task."""
    res = client.post("/tasks", json={"title": "Find Me"})
    task_id = res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_task_not_found(client):
    """GET /tasks/{id} should return 404 for non-existent task."""
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task(client):
    """PUT /tasks/{id} should update a task."""
    res = client.post("/tasks", json={"title": "Original"})
    task_id = res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated",
        "completed": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


def test_update_task_partial(client):
    """PUT /tasks/{id} with partial data should only update provided fields."""
    res = client.post("/tasks", json={"title": "Keep Me", "description": "Original Desc"})
    task_id = res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Keep Me"
    assert data["description"] == "Original Desc"
    assert data["completed"] is True


def test_update_task_not_found(client):
    """PUT /tasks/{id} should return 404 for non-existent task."""
    response = client.put("/tasks/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_task(client):
    """DELETE /tasks/{id} should remove a task."""
    res = client.post("/tasks", json={"title": "Delete Me"})
    task_id = res.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """DELETE /tasks/{id} should return 404 for non-existent task."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
