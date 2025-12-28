# In-Memory Todo CLI Application

A command-line todo application that allows users to manage tasks entirely in memory.

## Features

- Add new tasks with title and description
- View all tasks with their status
- Update existing task details
- Delete tasks
- Mark tasks as complete or incomplete

## Usage

Run the application with Python:

```bash
python src/main.py
```

### Available Options

1. **Add Task**: Create a new task with a title and optional description
2. **View Tasks**: Display all tasks with their ID, title, description, and completion status
3. **Mark Complete/Incomplete**: Toggle task status (complete/incomplete) or choose specific action
4. **Update Task**: Modify an existing task's title or description
5. **Delete Task**: Remove a task from the list (with confirmation)
6. **Exit**: Quit the application

## Project Structure

```
src/
├── todo_app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main_menu.py
│   └── main.py
```

## Technology Stack

- Python 3.13+
- Standard Python libraries only
- In-memory storage (no persistence)
- All data is discarded when the application exits