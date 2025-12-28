# Quickstart Guide: In-Memory Todo CLI Application

## Running the Application

1. Ensure you have Python 3.13+ installed on your system
2. Navigate to the project directory
3. Run the application with: `python src/main.py`
4. The application will present a menu with available options

## Available Commands

- **Add Task**: Select option 1 to add a new task with title and description
- **View Tasks**: Select option 2 to see all tasks with their status
- **Update Task**: Select option 3 to modify an existing task
- **Delete Task**: Select option 4 to remove a task
- **Mark Complete/Incomplete**: Select option 5 to toggle task completion status
- **Exit**: Select option 6 to quit the application

## Example Usage

1. Start the application
2. Choose option 1 to add a task
3. Enter the task title when prompted
4. Enter the task description when prompted
5. The task will be added with a unique ID
6. Choose option 2 to view all tasks
7. Continue using the menu to manage your tasks

## Important Notes

- All tasks are stored in memory only and will be lost when the application exits
- Task IDs are automatically generated as unique numbers
- Invalid menu selections will show an error message and return to the main menu
- Invalid task IDs in operations will show an appropriate error message