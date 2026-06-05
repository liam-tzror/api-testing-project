import requests

BASE_URL = "http://localhost:3000"


def login():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "liam",
        "password": "1234"
    })
    token = response.json()["token"]
    return token


def test_login_wrong_password():
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "liam",
        "password": "1234512"
    })
    if response.status_code == 401:
        print("passed - wrong password blocked")
    else:
        print("failed - should have blocked")


def test_get_tasks(token):
    response = requests.get(f"{BASE_URL}/tasks", headers={
        "authorization": token
    })
    if response.status_code == 200:
        print("passed - get tasks works")
    else:
        print("failed - get tasks not working")


def test_create_task(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "test task"}
                             )
    if response.status_code == 201:
        print("passed - create task works")
    else:
        print("failed - create task not working")
    
    return response.json()


def test_create_task_without_title(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={}
                             )
    if response.status_code == 400:
        print("passed - error when no title")
    else:
        print("failed - should have returned error")
        
        
        
def test_delete_task(token, task_id):
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}",
                             headers={"authorization": token})
    if response.status_code == 200:
        print("passed - the task is deleted")
    else:
        print("failed - delete task not working")
        
        
def test_update_task(token, task_id):
    response = requests.put(f"{BASE_URL}/tasks/{task_id}",
                             headers={"authorization": token},
                             json={"status": "done"}
                             )
    if response.status_code == 200:
        print("passed - update task works")
    else:
        print("failed - update task not working")
        
        
def test_create_task_with_numbers(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": 1234}
                             )
    if response.status_code == 400:
        print("passed - number in title blocked")
    else:
        print("failed - should have blocked number")
        
        
def test_create_task_with_spaces(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={"title": "     "})
    if response.status_code == 400:
        print("passed - spaces in title blocked")
    else:
        print("failed - should have blocked spaces")
        

def test_login_without_password():
    response = requests.post(f"{BASE_URL}/login",json={
        "username": "liam"
    })
    if response.status_code == 401:
        print("passed - password is empty")
    else:
        print("failed - should have blocked beacuse password is empty")


def test_get_task_invalid_id(token):
    response = requests.get(f"{BASE_URL}/tasks/99999",
                            headers={"authorization": token})
    if response.status_code == 404:
        print("passed - wrong id is blocked")
    else:
        print("failed - wrong id should have blocked")

    if "application/json" in response.headers["Content-Type"]:
        print("passed - response is JSON not HTML")
    else:
        print("failed - response is HTML not JSON - BUG!")
        
        
def test_register_existing_user():
    response = requests.post(f"{BASE_URL}/register",json={
        "username": "liam",
        "password": "1234"
    })
    if response.status_code == 400:
        print("passed - the user is already exists")
    else:
        print("failed - the user is created")
        
        
def test_create_task_long_title(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={
                                 "title": "a" * 500
                             })
    if response.status_code == 400:
        print("passed - long title blocked correctly")
    else:
        print("failed - long title should be blocked - BUG!")
        
        
        
def test_login_empty_username():
    response = requests.post(f"{BASE_URL}/login", json={
        "password": "1234"
    })
    if response.status_code == 400:
        print("passed - username is empty")
    else:
        print("failed - should have blocked beacuse username is empty")


def test_delete_nonexistent_task(token):
    response = requests.delete(f"{BASE_URL}/tasks/99999",
                               headers={"authorization": token})
    if response.status_code == 404:
        print("passed - there is no tasks with an id of 99999")
    else:
        print("failed - id was deleted - bug!")
        
        
        
def test_sql_injection():
    response = requests.post(f"{BASE_URL}/login",json={
        "username": "' OR '1'='1",
        "password": "' OR '1'='1"
    })
    if response.status_code == 401:
        print("passed - wrong user name and password")
    else:
        print("failed - logged in successfully bug!!!!")
        
    
    
def test_xss_attack(token):
    response = requests.post(f"{BASE_URL}/tasks",
                             headers={"authorization": token},
                             json={
                                 "title": "<script>alert('hacked')</script>"
                                 })
    if response.status_code == 400:
        print("passed - XSS attack blocked correctly")
    else:
        print("failed - XSS attack not blocked - BUG!")
        
        
        
def test_fake_token():
    response = requests.get(f"{BASE_URL}/tasks",
                             headers={"authorization": "fake-token-123"})
    if response.status_code == 401:
        print("passed - Incorrect TOKEN entry")
    else:
        print("failed - the wrong token have passed bug!!")
        

token = login()
test_login_wrong_password()
test_get_tasks(token)
test_create_task_without_title(token)
new_task = test_create_task(token)
test_update_task(token, new_task["id"])
test_delete_task(token, new_task["id"])
test_create_task_with_numbers(token)
test_create_task_with_spaces(token)
test_login_without_password()
test_get_task_invalid_id(token)
test_register_existing_user()
test_create_task_long_title(token)
test_login_empty_username()
test_delete_nonexistent_task(token)
test_sql_injection()
test_xss_attack(token)
test_fake_token()
