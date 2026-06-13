[# Project-py](https://roadmap.sh/projects/task-tracker)


1. Add some tasks:

Bash
python task_cli.py add "Buy groceries"
python task_cli.py add "Read a programming book"
(This will automatically create a cleanly-formatted tasks.json file in your directory).

2. List your current dashboard:

Bash
python task_cli.py list
3. Move a task to "In Progress":

Bash
python task_cli.py mark-in-progress 1
4. Filter tasks by status:

Bash
python task_cli.py list in-progress
python task_cli.py list todo
5. Update a task description:

Bash
python task_cli.py update 1 "Buy groceries and cook dinner"
6. Delete a finished task:

Bash
python task_cli.py delete 2
