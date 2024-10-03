import sys
import json
import os
from datetime import datetime

# File to store tasks
TASK_FILE = 'tasks.json'

# Ensure the file exists
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, 'w') as file:
        json.dump([], file)

# Helper function to load tasks
def load_tasks():
    with open(TASK_FILE, 'r') as file:
        return json.load(file)

# Helper function to save tasks
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Helper function to find task by id
def find_task(tasks, task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

# Command: Add a task
def add_task(description):
    tasks = load_tasks()
    task_id = max([task['id'] for task in tasks], default=0) + 1
    now = datetime.now().isoformat()
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

# Command: Update a task's description
def update_task(task_id, new_description):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        task['description'] = new_description
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

# Command: Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        tasks.remove(task)
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Task with ID {task_id} not found.")

# Command: Mark a task as in progress
def mark_in_progress(task_id):
    change_status(task_id, "in-progress")

# Command: Mark a task as done
def mark_done(task_id):
    change_status(task_id, "done")

# Command: Change the status of a task
def change_status(task_id, new_status):
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        task['status'] = new_status
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} marked as {new_status}.")
    else:
        print(f"Task with ID {task_id} not found.")

# Command: List all tasks, optionally filtered by status
def list_tasks(status_filter=None):
    tasks = load_tasks()
    if status_filter:
        filtered_tasks = [task for task in tasks if task['status'] == status_filter]
    else:
        filtered_tasks = tasks
    
    if filtered_tasks:
        for task in filtered_tasks:
            print(f"{task['id']}. {task['description']} - {task['status']} "
                  f"(Created at: {task['createdAt']}, Updated at: {task['updatedAt']})")
    else:
        print("No tasks found.")

# Command handler
def main():
    if len(sys.argv) < 2:
        print("Usage: task-cli <command> [arguments]")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: task-cli add <description>")
        else:
            add_task(sys.argv[2])

    elif command == "update":
        if len(sys.argv) < 4:
            print("Usage: task-cli update <task_id> <new_description>")
        else:
            try:
                update_task(int(sys.argv[2]), sys.argv[3])
            except ValueError:
                print("Invalid task ID. Must be an integer.")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: task-cli delete <task_id>")
        else:
            try:
                delete_task(int(sys.argv[2]))
            except ValueError:
                print("Invalid task ID. Must be an integer.")

    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-in-progress <task_id>")
        else:
            try:
                mark_in_progress(int(sys.argv[2]))
            except ValueError:
                print("Invalid task ID. Must be an integer.")

    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("Usage: task-cli mark-done <task_id>")
        else:
            try:
                mark_done(int(sys.argv[2]))
            except ValueError:
                print("Invalid task ID. Must be an integer.")

    elif command == "list":
        if len(sys.argv) == 3:
            list_tasks(sys.argv[2])
        else:
            list_tasks()

    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
