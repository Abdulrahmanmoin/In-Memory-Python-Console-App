#!/usr/bin/env python3
"""
Todo CLI Application
Main entry point for the in-memory todo application.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from todo_app.cli.main_menu import MainMenu


def main():
    """Main entry point for the application."""
    print("Todo CLI Application")
    print("Starting application...")

    # Initialize the main menu
    menu = MainMenu()

    # Main menu loop
    while True:
        print("\n--- Todo CLI Application ---")
        menu.show_add_task_option()
        menu.show_view_tasks_option()
        menu.show_mark_complete_option()
        menu.show_update_task_option()
        menu.show_delete_task_option()
        print("6. Exit")
        print("---------------------------")

        try:
            choice = input("Select an option (1-6): ").strip()

            if choice == "1":
                menu.add_task_cli()
            elif choice == "2":
                menu.view_tasks_cli()
            elif choice == "3":
                # Provide option to mark complete or toggle
                sub_choice = input("Choose action - 1: Mark Complete, 2: Mark Incomplete, 3: Toggle Status (1-3): ").strip()
                if sub_choice == "1":
                    menu.mark_task_complete_cli()
                elif sub_choice == "2":
                    menu.mark_task_incomplete_cli()
                elif sub_choice == "3":
                    menu.toggle_task_status_cli()
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            elif choice == "4":
                menu.update_task_cli()
            elif choice == "5":
                menu.delete_task_cli()
            elif choice == "6":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 6.")
        except KeyboardInterrupt:
            print("\n\nApplication interrupted. Exiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()