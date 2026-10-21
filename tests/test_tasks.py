from tests.conftest import register_and_login


def test_create_list_update_and_delete_task(client):
    headers = register_and_login(client, "owner@example.com")
    created = client.post(
        "/tasks",
        headers=headers,
        json={
            "title": "Prepare portfolio",
            "description": "Write project documentation",
            "priority": "high",
            "due_date": "2026-11-01T12:00:00Z",
        },
    )

    assert created.status_code == 201
    task = created.json()
    assert task["status"] == "pending"
    assert task["priority"] == "high"
    assert task["created_at"]
    assert task["updated_at"]

    listed = client.get("/tasks?status=pending&priority=high&limit=10", headers=headers)
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [task["id"]]
    assert client.get("/tasks?offset=1", headers=headers).json() == []

    retrieved = client.get(f"/tasks/{task['id']}", headers=headers)
    assert retrieved.status_code == 200
    assert retrieved.json()["title"] == "Prepare portfolio"
    assert client.get("/tasks/99999", headers=headers).status_code == 404

    updated = client.patch(
        f"/tasks/{task['id']}",
        headers=headers,
        json={"title": "Finish portfolio", "status": "completed"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "Finish portfolio"
    assert updated.json()["status"] == "completed"
    assert updated.json()["updated_at"]

    deleted = client.delete(f"/tasks/{task['id']}", headers=headers)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/tasks/{task['id']}", headers=headers).status_code == 404


def test_users_only_list_their_own_tasks(client):
    first_user = register_and_login(client, "first@example.com")
    second_user = register_and_login(client, "second@example.com")
    client.post("/tasks", headers=first_user, json={"title": "Private task"})

    response = client.get("/tasks", headers=second_user)

    assert response.status_code == 200
    assert response.json() == []


def test_user_cannot_read_update_or_delete_another_users_task(client):
    owner = register_and_login(client, "owner@example.com")
    other_user = register_and_login(client, "other@example.com")
    created = client.post("/tasks", headers=owner, json={"title": "Owner-only task"})
    task_id = created.json()["id"]

    assert client.get(f"/tasks/{task_id}", headers=other_user).status_code == 403
    assert (
        client.patch(
            f"/tasks/{task_id}", headers=other_user, json={"title": "Not allowed"}
        ).status_code
        == 403
    )
    assert client.delete(f"/tasks/{task_id}", headers=other_user).status_code == 403
    assert client.get(f"/tasks/{task_id}", headers=owner).status_code == 200


def test_task_validation_errors_return_422(client):
    headers = register_and_login(client, "validation@example.com")

    missing_title = client.post("/tasks", headers=headers, json={"priority": "high"})
    invalid_priority = client.post(
        "/tasks", headers=headers, json={"title": "Task", "priority": "urgent"}
    )
    empty_update = client.patch("/tasks/1", headers=headers, json={})
    null_status = client.patch("/tasks/1", headers=headers, json={"status": None})

    assert missing_title.status_code == 422
    assert invalid_priority.status_code == 422
    assert empty_update.status_code == 422
    assert null_status.status_code == 422


def test_task_endpoints_require_authentication(client):
    assert client.get("/tasks").status_code == 401
    assert client.post("/tasks", json={"title": "No token"}).status_code == 401
