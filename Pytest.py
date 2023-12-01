import requests

ENDPOINT = "https://todo.pixegami.io/"


def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    payload = {
        "content": "my test content",
        "user_id": "tester",
        "is_done": False
    }
    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()

    task_id = data["task"]["task1"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task_status():
    task_id = {"task1"}
    update_payload = {"is_done": True}
    update_task_response = requests.post(ENDPOINT + f"/update-task/{task_id}", json=update_payload)
    assert update_task_response.status_code == 200

    get_updated_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_updated_task_response.status_code == 200

    updated_task_data = get_updated_task_response.json()
    assert updated_task_data["is_done"] == update_payload["is_done"]

    task_id = {"task2"}
    update_payload = {"is_done": True}
    update_task_response = requests.post(ENDPOINT + f"/update-task/{task_id}", json=update_payload)
    assert update_task_response.status_code == 200

    get_updated_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_updated_task_response.status_code == 200

    updated_task_data = get_updated_task_response.json()
    assert updated_task_data["is_done"] == update_payload["is_done"]


def test_can_delete_task():
    task_id = {"task2"}
    delete_task_response = requests.delete(ENDPOINT + f"/delete-task/{task_id}")
    assert delete_task_response.status_code == 200

    get_deleted_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_deleted_task_response.status_code == 404  # 404 Not Found


def test_can_list_all_tasks():
    list_tasks_response = requests.get(ENDPOINT + "/list-tasks")
    assert list_tasks_response.status_code == 200
    tasks_data = list_tasks_response.json()
    assert isinstance(tasks_data, list)


def test_can_filter_tasks_by_user():
    user_id = "tester"
    filter_tasks_response = requests.get(ENDPOINT + f"/filter-tasks?user_id={user_id}")
    assert filter_tasks_response.status_code == 200
    filtered_tasks_data = filter_tasks_response.json()
    for task in filtered_tasks_data:
        assert task["user_id"] == user_id
    

def test_invalid_authentication():
    response = requests.get(ENDPOINT + "/protected-endpoint", auth=("invalid_user", "invalid_password"))
    assert response.status_code == 401  # 401 Unauthorized


def test_can_mark_task_as_high_priority():
    task_id = "task1"
    mark_priority_payload = {"priority": "high"}
    mark_priority_response = requests.post(ENDPOINT + f"/mark-priority/{task_id}", json=mark_priority_payload)
    assert mark_priority_response.status_code == 200

    get_marked_priority_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_marked_priority_response.status_code == 200

    marked_priority_data = get_marked_priority_response.json()
    assert marked_priority_data["priority"] == "high"


def test_can_archive_completed_tasks():
    task_id = "task1"
    update_payload = {"is_done": True}
    update_task_response = requests.post(ENDPOINT + f"/update-task/{task_id}", json=update_payload)
    assert update_task_response.status_code == 200

    archive_completed_payload = {"archive_completed": True}
    archive_completed_response = requests.post(ENDPOINT + "/archive-completed-tasks", json=archive_completed_payload)
    assert archive_completed_response.status_code == 200

    get_archived_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_archived_task_response.status_code == 404  # 404 Not Found
