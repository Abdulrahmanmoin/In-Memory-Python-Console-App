# Data Model: In-Memory Todo CLI Application

## Task Entity

**Name**: Task
**Fields**:
- `id` (integer): Unique identifier for the task, auto-generated
- `title` (string): Title/description of the task, required
- `description` (string): Detailed description of the task, optional
- `completed` (boolean): Status indicating if the task is completed (true) or pending (false)

**Validation Rules**:
- `id` must be unique within the task list
- `title` must not be empty or only whitespace
- `description` can be empty but defaults to empty string if not provided
- `completed` defaults to False when creating a new task

**State Transitions**:
- `pending` (completed=False) → `completed` (completed=True) when user marks task complete
- `completed` (completed=True) → `pending` (completed=False) when user marks task incomplete

## Task List Entity

**Name**: Task List
**Fields**:
- `tasks` (list of Task objects): Collection of all tasks in memory
- `next_id` (integer): Counter for generating next unique task ID

**Operations**:
- Add task: Append new task to the list
- Get task by ID: Find task with matching ID
- Update task: Modify existing task properties
- Delete task: Remove task from the list
- Mark complete/incomplete: Update completion status of a task