"""
Main menu for the todo CLI application.
Handles user input and interaction for all task operations.
"""

from typing import Optional
from src.todo_app.services.task_service import TaskList


class MainMenu:
    """
    CLI interface for the todo application.
    Provides methods for all user interactions with tasks.
    """

    def __init__(self):
        """
        Initialize the main menu with a task list.
        """
        self.task_list = TaskList()

    def prompt_task_title(self) -> str:
        """
        Prompt the user for a task title.

        Returns:
            str: The title entered by the user
        """
        return input("Enter task title: ").strip()

    def prompt_task_description(self) -> str:
        """
        Prompt the user for a task description.

        Returns:
            str: The description entered by the user
        """
        return input("Enter task description (optional): ").strip()

    def add_task_cli(self) -> bool:
        """
        CLI function to add a task via user input.

        Returns:
            bool: True if task was added successfully, False otherwise
        """
        try:
            title = self.prompt_task_title()

            # Validate title input
            if not title:
                print("Error: Task title cannot be empty.")
                return False

            description = self.prompt_task_description()
            task = self.task_list.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}, Title: {task.title}")
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error adding task: {e}")
            return False

    def view_tasks_cli(self) -> None:
        """
        CLI function to display all tasks.
        """
        tasks = self.task_list.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print("\n--- All Tasks ---")
        for task in tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"ID: {task.id} | [{status}] | Title: {task.title}")
            if task.description:
                print(f"      Description: {task.description}")
        print("-----------------\n")

    def format_task_display(self, task) -> str:
        """
        Format task display with ID, title, description, and status.

        Args:
            task: The task object to format

        Returns:
            str: Formatted string representation of the task
        """
        status = "Completed" if task.completed else "Pending"
        return f"ID: {task.id} | [{status}] | Title: {task.title}"

    def handle_empty_task_list(self) -> None:
        """
        Handle empty task list case with appropriate message.
        """
        print("No tasks found.")

    def add_visual_distinction(self, task) -> str:
        """
        Add visual distinction between completed and pending tasks in display.

        Args:
            task: The task object to format

        Returns:
            str: Formatted string with visual distinction
        """
        status_symbol = "✓" if task.completed else "○"
        status_text = "Completed" if task.completed else "Pending"
        return f"[{status_symbol}] ID: {task.id} | {status_text} | Title: {task.title}"

    def prompt_task_id(self) -> int:
        """
        Prompt the user for a task ID.

        Returns:
            int: The task ID entered by the user
        """
        while True:
            try:
                task_id = int(input("Enter task ID: "))
                return task_id
            except ValueError:
                print("Error: Please enter a valid number for task ID.")

    def mark_task_complete_cli(self) -> bool:
        """
        CLI function to mark task complete/incomplete.

        Returns:
            bool: True if task was marked successfully, False otherwise
        """
        task_id = self.prompt_task_id()
        success = self.task_list.mark_task_complete(task_id)

        if success:
            print(f"Task {task_id} marked as complete.")
            return True
        else:
            print(f"Error: Task with ID {task_id} not found.")
            return False

    def mark_task_incomplete_cli(self) -> bool:
        """
        CLI function to mark task incomplete.

        Returns:
            bool: True if task was marked successfully, False otherwise
        """
        task_id = self.prompt_task_id()
        success = self.task_list.mark_task_incomplete(task_id)

        if success:
            print(f"Task {task_id} marked as incomplete.")
            return True
        else:
            print(f"Error: Task with ID {task_id} not found.")
            return False

    def toggle_task_status_cli(self) -> bool:
        """
        CLI function to toggle task status.

        Returns:
            bool: True if task status was toggled successfully, False otherwise
        """
        task_id = self.prompt_task_id()
        success = self.task_list.toggle_task_status(task_id)

        if success:
            task = self.task_list.get_task_by_id(task_id)
            status = "complete" if task.completed else "incomplete"
            print(f"Task {task_id} marked as {status}.")
            return True
        else:
            print(f"Error: Task with ID {task_id} not found.")
            return False

    def show_mark_complete_option(self) -> None:
        """
        Show the 'Mark Complete/Incomplete' option in the main menu.
        """
        print("3. Mark Complete/Incomplete")

    def display_confirmation(self, message: str) -> None:
        """
        Display a confirmation message to the user.

        Args:
            message (str): The confirmation message to display
        """
        print(message)

    def handle_invalid_input(self, error_message: str) -> None:
        """
        Handle invalid input by displaying an error message.

        Args:
            error_message (str): The error message to display
        """
        print(f"Error: {error_message}")

    def show_add_task_option(self) -> None:
        """
        Show the 'Add Task' option in the main menu.
        """
        print("1. Add Task")

    def get_task_id_for_update(self) -> int:
        """
        CLI function to get task ID for update.

        Returns:
            int: The task ID entered by the user
        """
        while True:
            try:
                task_id = int(input("Enter task ID to update: "))
                return task_id
            except ValueError:
                print("Error: Please enter a valid number for task ID.")

    def get_new_title_for_task(self) -> str:
        """
        CLI function to get new title for task.

        Returns:
            str: The new title entered by the user
        """
        return input("Enter new title (leave blank to keep current): ").strip()

    def get_new_description_for_task(self) -> str:
        """
        CLI function to get new description for task.

        Returns:
            str: The new description entered by the user
        """
        return input("Enter new description (leave blank to keep current): ").strip()

    def update_task_cli(self) -> bool:
        """
        CLI function to update task details.

        Returns:
            bool: True if task was updated successfully, False otherwise
        """
        task_id = self.get_task_id_for_update()

        # Check if task exists
        task = self.task_list.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"Current task: [{task.title}] - {task.description}")

        new_title_input = self.get_new_title_for_task()
        new_description_input = self.get_new_description_for_task()

        # Prepare update parameters
        title_update = new_title_input if new_title_input else None
        description_update = new_description_input if new_description_input else None

        # Only update if there's something to update
        if title_update is None and description_update is None:
            print("No changes provided. Task not updated.")
            return False

        try:
            success = self.task_list.update_task(task_id, title_update, description_update)

            if success:
                print(f"Task {task_id} updated successfully.")
                return True
            else:
                print(f"Error: Task with ID {task_id} could not be updated.")
                return False
        except ValueError as e:
            print(f"Error: {e}")
            return False

    def get_task_id_for_deletion(self) -> int:
        """
        CLI function to get task ID for deletion.

        Returns:
            int: The task ID entered by the user
        """
        while True:
            try:
                task_id = int(input("Enter task ID to delete: "))
                return task_id
            except ValueError:
                print("Error: Please enter a valid number for task ID.")

    def delete_task_cli(self) -> bool:
        """
        CLI function to delete task.

        Returns:
            bool: True if task was deleted successfully, False otherwise
        """
        task_id = self.get_task_id_for_deletion()

        # Check if task exists before deletion
        task = self.task_list.get_task_by_id(task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            return False

        print(f"About to delete task: [{task.title}]")

        # Confirm deletion
        confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes']:
            print("Task deletion cancelled.")
            return False

        success = self.task_list.delete_task(task_id)

        if success:
            print(f"Task {task_id} deleted successfully.")
            return True
        else:
            print(f"Error: Task with ID {task_id} could not be deleted.")
            return False

    def show_update_task_option(self) -> None:
        """
        Show the 'Update Task' option in the main menu.
        """
        print("4. Update Task")

    def show_delete_task_option(self) -> None:
        """
        Show the 'Delete Task' option in the main menu.
        """
        print("5. Delete Task")

    def show_view_tasks_option(self) -> None:
        """
        Show the 'View Tasks' option in the main menu.
        """
        print("2. View Tasks")