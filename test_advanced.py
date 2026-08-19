import requests
import pytest

BASE_URL = "http://localhost:3000"

@pytest.fixture
def token():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "liam",
        "password": "1234"
    })
    return response.json()["token"]

@pytest.mark.parametrize("bad_title", [
    21345,
    "<script>alert('hacked')</script>",
    "     ",
    "a" * 500
])

def test_invalid_titles(token, bad_title):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": bad_title})
    assert response.status_code == 400
    

def test_create_task_returns_correct_title(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test task"})
    assert response.status_code == 201
    assert response.json()["title"] == "test task"
    

def test_empty_title_error_message(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": ""})
    assert response.status_code == 400
    assert response.json()["error"] == "Title is required"
    
    
def test_create_task_returns_id(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test title"})
    assert response.status_code == 201
    assert "id" in response.json()
    
    
def test_delete_task(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test2"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}",
                             headers={"authorization": token})
    assert response.status_code == 200
    
    response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers={
        "authorization": token
    })
    assert response.status_code == 404
    
    
    
def test_update_task(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test3"})
    assert response.status_code == 201
    task_id = response.json()["id"]
    
    response = requests.put(f"{BASE_URL}/tasks/{task_id}",
                            headers={"authorization": token},
                            json={"status": "done"})
    assert response.status_code == 200
    
    
def test_no_token():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 401
    
    
def test_missing_title_field(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={})
    assert response.status_code == 400
    assert response.json()["error"] == "Title is required"