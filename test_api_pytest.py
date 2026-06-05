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


def test_get_tasks(token):
    response = requests.get(f"{BASE_URL}/tasks", headers={
        "authorization": token
    })
    assert response.status_code == 200


def test_create_task(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test task"})
    assert response.status_code == 201


def test_login_wrong_password():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "liam",
        "password": "wrong"
    })
    assert response.status_code == 401
    
    
    
def test_create_task_without_title(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={
                                 "title": ""
                             })
    assert response.status_code == 400
    
    
def test_delete_task(token):
    new_task = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "task to delete"})
    task_id = new_task.json()["id"]
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}",
                               headers={"authorization": token})
    assert response.status_code == 200
    
    
    
def test_update_task(token):
    new_task = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "task to update"})
    task_id = new_task.json()["id"]
    response = requests.put(f"{BASE_URL}/tasks/{task_id}",
                            headers={"authorization": token},
                            json={
                                "status": "done"
                            })
    assert response.status_code == 200
    
    
    
def test_create_task_with_numbers(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={
                                 "title": 21345
                             })
    assert response.status_code == 400
    
    
    
def test_xss_attack(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={
                                 "title": "<script>alert('hacked')</script>"
                             })
    assert response.status_code == 400
    
    
    
def test_fake_token():
    response = requests.get(f"{BASE_URL}/tasks",
                            headers={"authorization": "limlim_12"})
    assert response.status_code == 401