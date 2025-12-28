"""
Task service for the todo application.
Handles all business logic for task operations with in-memory storage.
"""

from typing import List, Optional
from src.todo_app.models.task import Task


class TaskList:
    """
    Service class that manages a collection of tasks in memory.
    Provides methods for all required task operations.
    """

    def __init__(self):
        """
        Initialize a new TaskList instance with empty task list and ID counter.
        """
        self.tasks: List[Task] = []
        self.next_id: int = 1

    def add_task(self, title: str, description: str = "") -> Task:
        """
        Add a new task to the list with a unique ID.

        Args:
            title (str): Title of the task
            description (str): Description of the task (optional)

        Returns:
            Task: The newly created task object

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        task = Task(self.next_id, title, description)
        self.tasks.append(task)
        self.next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the list.

        Returns:
            List[Task]: A list of all tasks
        """
        return self.tasks.copy()  # Return a copy to prevent external modification

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find a task by its ID.

        Args:
            task_id (int): The ID of the task to find

        Returns:
            Optional[Task]: The task if found, None otherwise
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, title: str = None, description: str = None) -> bool:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The ID of the task to update
            title (str, optional): New title for the task
            description (str, optional): New description for the task

        Returns:
            bool: True if the task was updated, False if task was not found

        Raises:
            ValueError: If new title is empty or contains only whitespace
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Update title if provided
        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty or contain only whitespace")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.

        Args:
            task_id (int): The ID of the task to delete

        Returns:
            bool: True if the task was deleted, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        return True

    def mark_task_complete(self, task_id: int) -> bool:
        """
        Mark a task as complete.

        Args:
            task_id (int): The ID of the task to mark complete

        Returns:
            bool: True if the task was marked complete, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = True
        return True

    def mark_task_incomplete(self, task_id: int) -> bool:
        """
        Mark a task as incomplete.

        Args:
            task_id (int): The ID of the task to mark incomplete

        Returns:
            bool: True if the task was marked incomplete, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = False
        return True

    def toggle_task_status(self, task_id: int) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id (int): The ID of the task to toggle

        Returns:
            bool: True if the task status was toggled, False if task was not found
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        task.completed = not task.completed
        return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.

        Returns:
            int: The number of tasks in the list
        """
        return len(self.tasks)

    def clear_all_tasks(self) -> None:
        """
        Clear all tasks from the list and reset the ID counter.
        """
        self.tasks.clear()
        self.next_id = 1

    def get_completed_tasks(self) -> List[Task]:
        """
        Get all completed tasks.

        Returns:
            List[Task]: A list of completed tasks
        """
        return [task for task in self.tasks if task.completed]

    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending tasks.

        Returns:
            List[Task]: A list of pending tasks
        """
        return [task for task in self.tasks if not task.completed]