import requests
import time

BASE_URL = "http://127.0.0.1:8000/api/reminders"

# Test scheduling a reminder
def test_schedule_reminder():
    reminder_data = {
        "task_id": 1,
        "title": "Team Meeting",
        "due_date": "2025-02-25",
        "priority": "High",
        "notify_time": "2025-02-24T10:00:00"
    }
    response = requests.post(BASE_URL, json=reminder_data)
    print("Schedule Reminder Response:", response.json())

# Test updating a reminder
def test_update_reminder():
    updated_data = {
        "task_id": 1,
        "title": "Updated Meeting",
        "due_date": "2025-02-26",
        "priority": "Medium",
        "notify_time": "2025-02-25T09:00:00"
    }
    response = requests.put(f"{BASE_URL}/1", json=updated_data)
    print("Update Reminder Response:", response.json())

# Test retrieving reminders
def test_get_reminders():
    response = requests.get(BASE_URL)
    print("Get Reminders Response:", response.json())

# Test deleting a reminder
def test_delete_reminder():
    response = requests.delete(f"{BASE_URL}/1")
    print("Delete Reminder Response:", response.json())

if __name__ == "__main__":
    print("Starting Microservice Test Program...")
    test_schedule_reminder()
    time.sleep(2)  # Wait for processing
    test_update_reminder()
    time.sleep(2)
    test_get_reminders()
    time.sleep(2)
    test_delete_reminder()
    print("Microservice Test Completed.")