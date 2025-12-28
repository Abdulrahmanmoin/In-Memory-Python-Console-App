"""
Task model for the todo application.
Represents a single todo item with unique identifier, title, description, and completion status.
"""

from typing import Union


class Task:
    """
    Represents a single todo item with unique identifier, title, description, and completion status.
    """

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task instance.

        Args:
            task_id (int): Unique identifier for the task
            title (str): Title of the task (required)
            description (str): Detailed description of the task (optional, defaults to empty string)
            completed (bool): Status indicating if the task is completed (defaults to False)

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty or contain only whitespace")

        self.id = task_id
        self.title = title.strip()
        self.description = description
        self.completed = completed

    def __str__(self) -> str:
        """
        Return a string representation of the task.

        Returns:
            str: Formatted string representation of the task
        """
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}. {self.title} - {self.description}"

    def __repr__(self) -> str:
        """
        Return a detailed string representation of the task.

        Returns:
            str: Detailed representation for debugging purposes
        """
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self) -> dict:
        """
        Convert the task to a dictionary representation.

        Returns:
            dict: Dictionary representation of the task
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task instance from a dictionary.

        Args:
            data (dict): Dictionary containing task data

        Returns:
            Task: New Task instance
        """
        return cls(
            task_id=data['id'],
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )