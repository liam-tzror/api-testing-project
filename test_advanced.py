import os
import requests
import pytest

BASE_URL = os.environ.get("BASE_URL", "http://localhost:3000")

@pytest.fixture
def token():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "liam",
        "password": "1234"
    })
    return response.json()["token"]


@pytest.fixture
def session(token):
    s = requests.Session()
    s.headers.update({"authorization": token})
    return s


@pytest.fixture
def created_task(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": "testing"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    yield task_id
    response = session.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200


def test_get_created_task(session, created_task):
    task_id = created_task
    response = session.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_create_task_returns_correct_title(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": "test task"})
    assert response.status_code == 201
    assert response.json()["title"] == "test task"


def test_create_task_returns_id(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": "test title"})
    assert response.status_code == 201
    assert "id" in response.json()


def test_missing_title_field(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={})
    assert response.status_code == 400
    assert response.json()["error"] == "Title is required"


def test_empty_title_error_message(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": ""})
    assert response.status_code == 400
    assert response.json()["error"] == "Title is required"


@pytest.mark.parametrize("bad_title", [
    21345,
    "<script>alert('hacked')</script>",
    "     ",
    "a" * 500
])
def test_invalid_titles(session, bad_title):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": bad_title})
    assert response.status_code == 400


def test_update_task(session, created_task):
    task_id = created_task

    response = session.put(f"{BASE_URL}/tasks/{task_id}",
                            json={"status": "done"})
    assert response.status_code == 200


@pytest.mark.parametrize("bad_status", ["None", "בננה", "123", ""])
def test_invalid_status_update(session, created_task, bad_status):
    task_id = created_task
    response = session.put(f"{BASE_URL}/tasks/{task_id}",
                            json={"status": bad_status})
    assert response.status_code == 400


def test_delete_task(session):
    response = session.post(f"{BASE_URL}/tasks",
                             json={"title": "test2"})
    assert response.status_code == 201
    task_id = response.json()["id"]

    response = session.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200

    response = session.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 404


def test_no_token():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 401