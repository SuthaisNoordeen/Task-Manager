import requests
import json
import sys

BASE_URL = "http://localhost:3000"

def test_health_endpoint():
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(" Health endpoint working")
            print(f"   Response: {data}")
            return True
        else:
            print(f" Health endpoint failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Connection error: Server might not be running")
        return False

def test_get_tasks():
    try:
        response = requests.get(f"{BASE_URL}/api/tasks")
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Get tasks endpoint working, found {len(tasks)} tasks")
            if len(tasks) > 0:
                print(f"   First task: {tasks[0]['title']}")
            return True
        else:
            print(f" Get tasks endpoint failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Connection error: Server might not be running")
        return False

def test_add_task():
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task created by the test script"
        }
        response = requests.post(
            f"{BASE_URL}/api/tasks",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        if response.status_code == 201:
            data = response.json()
            print("✅ Add task endpoint working")
            print(f"   Response: {data['message']}")
            if 'task' in data:
                print(f"   Created task ID: {data['task']['id']}")
                return data['task']['id']
            return True
        else:
            print(f" Add task endpoint failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Connection error: Server might not be running")
        return False

def test_update_task(task_id):
    try:
        update_data = {
            "completed": True
        }
        response = requests.put(
            f"{BASE_URL}/api/tasks/{task_id}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(update_data)
        )
        if response.status_code == 200:
            data = response.json()
            print(" Update task endpoint working")
            print(f"   Response: {data['message']}")
            return True
        else:
            print(f" Update task endpoint failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Connection error: Server might not be running")
        return False

def test_delete_task(task_id):
    try:
        response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Delete task endpoint working")
            print(f"   Response: {data['message']}")
            return True
        else:
            print(f" Delete task endpoint failed with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(" Connection error: Server might not be running")
        return False

def run_tests():
    print("🔍 Testing Task Manager API...")
    print("-" * 50)
    
    # Test health endpoint
    if not test_health_endpoint():
        print("\n Server health check failed. Make sure the server is running.")
        return False
    
    print("-" * 50)
    
    # Test get tasks
    if not test_get_tasks():
        print("\n Failed to get tasks.")
        return False
    
    print("-" * 50)
    
    # Test add task
    task_id = test_add_task()
    if not task_id:
        print("\n Failed to add task.")
        return False
    
    print("-" * 50)
    
    # Test update task
    if not test_update_task(task_id):
        print("\n Failed to update task.")
        return False
    
    print("-" * 50)
    
    # Test delete task
    if not test_delete_task(task_id):
        print("\n Failed to delete task.")
        return False
    
    print("-" * 50)
    print("\nAll tests passed successfully!")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 