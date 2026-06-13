import json
import sys
import os
from datetime import datetime

# File where tasks will be stored in the current working directory
DATA_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the JSON file. Creates an empty file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Saves the tasks list back to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def get_next_id(tasks):
    """Generates a unique incremental ID."""
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def current_timestamp():
    """Returns the current date and time formatted as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# --- Core Features ---

def add_task(description):
    if not description.strip():
        print("Error: Task description cannot be empty.")
        return
    
    tasks = load_tasks()
    new_task = {
        "id": get_next_id(tasks),
        "description": description,
        "status": "todo",
        "createdAt": current_timestamp(),
        "updatedAt": current_timestamp()
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = current_timestamp()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    tasks = load_tasks()
    initial_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]
    
    if len(tasks) == initial_length:
        print(f"Error: Task with ID {task_id} not found.")
    else:
        save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")

def update_status(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = new_status
            task["updatedAt"] = current_timestamp()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}.")
            return
    print(f"Error: Task with ID {task_id} not found.")

def list_tasks(status_filter=None):
    tasks = load_tasks()
    
    if status_filter:
        if status_filter not in ["todo", "in-progress", "done"]:
            print("Error: Invalid filter. Use 'todo', 'in-progress', or 'done'.")
            return
        tasks = [task for task in tasks if task["status"] == status_filter]

    if not tasks:
        print("No tasks found.")
        return

    print(f"\n{'ID':<5} | {'Description':<40} | {'Status':<12} | {'Updated At'}")
    print("-" * 80)
    for task in tasks:
        print(f"{task['id']:<5} | {task['description']:<40} | {task['status']:<12} | {task['updatedAt']}")
    print()

# --- Command Line Argument Routing ---

def print_help():
    print("""
Usage: python task_cli.py [command] [arguments]

Commands:
  add "[description]"         Add a new task
  update [id] "[description]" Update a task's description
  delete [id]                 Delete a task
  mark-in-progress [id]       Mark a task as in-progress
  mark-done [id]              Mark a task as done
  list                        List all tasks
  list [status]               List tasks by status (todo, in-progress, done)
    """)

def main():
    # sys.argv holds the positional arguments passed via command line
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Missing task description.")
            else:
                add_task(sys.argv[2])

        elif command == "update":
            if len(sys.argv) < 4:
                print("Error: Missing task ID or new description.")
            else:
                update_task(int(sys.argv[2]), sys.argv[3])

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Missing task ID.")
            else:
                delete_task(int(sys.argv[2]))

        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("Error: Missing task ID.")
            else:
                update_status(int(sys.argv[2]), "in-progress")

        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("Error: Missing task ID.")
            else:
                update_status(int(sys.argv[2]), "done")

        elif command == "list":
            if len(sys.argv) == 3:
                list_tasks(sys.argv[2].lower())
            else:
                list_tasks()

        else:
            print(f"Unknown command: '{command}'")
            print_help()

    except ValueError:
        print("Error: Invalid Task ID format. Expected an integer.")

if __name__ == "__main__":
    main()
