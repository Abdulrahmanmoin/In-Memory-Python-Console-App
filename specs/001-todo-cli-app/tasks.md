# Implementation Tasks: In-Memory Todo CLI Application

**Feature**: In-Memory Todo CLI Application
**Branch**: 001-todo-cli-app
**Created**: 2025-12-28
**Status**: Draft
**Based on**: Plan from `/specs/001-todo-cli-app/plan.md`

## Implementation Strategy

Build the application incrementally following the user story priorities:
- MVP: User Story 1 (Add New Task) - minimal functionality to create tasks
- Increment 1: User Story 2 (View All Tasks) - view created tasks
- Increment 2: User Story 3 (Mark Complete/Incomplete) - toggle task status
- Increment 3: User Story 4 (Update Existing Task) - modify task details
- Increment 4: User Story 5 (Delete Task) - remove tasks
- Final: Polish and integration testing

## Dependencies

- User Story 1 (Add Task) → Foundation for all other stories
- User Story 2 (View Tasks) → Depends on Task model from Story 1
- User Story 3 (Mark Complete) → Depends on Task model and Task List service
- User Story 4 (Update Task) → Depends on Task model and Task List service
- User Story 5 (Delete Task) → Depends on Task model and Task List service

## Parallel Execution Examples

- Unit tests can be developed in parallel with implementation tasks (T020-T030 can run alongside T001-T019)
- UI components can be developed in parallel after models and services exist
- Integration tests can run in parallel after individual stories are complete

---

## Phase 1: Project Setup

### Goal
Initialize the project structure with necessary files and dependencies following the planned architecture.

### Independent Test Criteria
- Project structure matches implementation plan
- Python files have proper `__init__.py` files
- Main entry point can be executed without errors

### Tasks

- [X] T001 Create project directory structure: src/todo_app/, src/todo_app/models/, src/todo_app/services/, src/todo_app/cli/
- [X] T002 Create __init__.py files in all directories: src/todo_app/__init__.py, src/todo_app/models/__init__.py, src/todo_app/services/__init__.py, src/todo_app/cli/__init__.py
- [X] T003 Create basic main.py entry point in src/main.py that prints "Todo CLI Application"
- [X] T004 Create basic README.md with project description

---

## Phase 2: Foundational Components

### Goal
Implement core data models and services that all user stories depend on.

### Independent Test Criteria
- Task model can be instantiated with all required properties
- Task service can perform basic operations on tasks
- Unique ID generation works correctly

### Tasks

- [X] T005 [P] [US1] Create Task model class in src/todo_app/models/task.py with id, title, description, completed properties
- [X] T006 [P] [US1] Create TaskList service in src/todo_app/services/task_service.py with in-memory storage
- [X] T007 [P] [US1] Implement unique ID generation in TaskList service with auto-incrementing counter
- [X] T008 [P] [US1] Implement task validation rules in Task model (title not empty)
- [X] T009 [P] [US1] Add proper __init__.py exports for models and services

---

## Phase 3: User Story 1 - Add New Task (Priority: P1)

### Goal
Enable users to add new tasks to the todo list with title and description.

### Independent Test Criteria
- User can add a task with title and description
- Task is assigned a unique ID automatically
- Confirmation message is displayed after adding task

### Acceptance Scenarios
1. Given user wants to add a new task, When user runs add command with title and description, Then system creates task with unique ID and displays confirmation message
2. Given user enters invalid input for task title, When user runs add command, Then system displays helpful error message and allows re-entry

### Tasks

- [X] T010 [US1] Create add_task method in TaskList service that accepts title and description
- [X] T011 [US1] Implement CLI function to prompt user for task title in src/todo_app/cli/main_menu.py
- [X] T012 [US1] Implement CLI function to prompt user for task description in src/todo_app/cli/main_menu.py
- [X] T013 [US1] Create CLI function to add task via user input in src/todo_app/cli/main_menu.py
- [X] T014 [US1] Add input validation for task title (not empty)
- [X] T015 [US1] Display confirmation message after successful task creation
- [X] T016 [US1] Add error handling for invalid input in src/todo_app/cli/main_menu.py
- [X] T017 [US1] Update main menu to include "Add Task" option

---

## Phase 4: User Story 2 - View All Tasks (Priority: P1)

### Goal
Display all tasks with their ID, title, description, and completion status.

### Independent Test Criteria
- All tasks are displayed with complete information
- Empty state is handled properly with appropriate message
- Completed tasks are visually distinguished from pending tasks

### Acceptance Scenarios
1. Given user has multiple tasks in the system, When user runs view command, Then system displays all tasks with ID, title, description, and completion status
2. Given user has no tasks in the system, When user runs view command, Then system displays appropriate message indicating no tasks exist

### Tasks

- [X] T018 [US2] Create get_all_tasks method in TaskList service that returns all tasks
- [X] T019 [US2] Implement view_tasks CLI function in src/todo_app/cli/main_menu.py to display all tasks
- [X] T020 [US2] Format task display with ID, title, description, and status (completed/pending)
- [X] T021 [US2] Handle empty task list case with appropriate message
- [X] T022 [US2] Add visual distinction between completed and pending tasks in display
- [X] T023 [US2] Update main menu to include "View Tasks" option

---

## Phase 5: User Story 3 - Mark Task Complete/Incomplete (Priority: P2)

### Goal
Allow users to toggle the completion status of tasks by ID.

### Independent Test Criteria
- Task status can be changed from pending to completed and vice versa
- Error handling for invalid task IDs
- Confirmation message after status change

### Acceptance Scenarios
1. Given user has a pending task, When user runs mark complete command with valid task ID, Then system updates task status to complete and displays confirmation
2. Given user provides invalid task ID, When user runs mark command, Then system displays helpful error message

### Tasks

- [X] T024 [US3] Create mark_task_complete method in TaskList service that accepts task ID
- [X] T025 [US3] Create mark_task_incomplete method in TaskList service that accepts task ID
- [X] T026 [US3] Create toggle_task_status method in TaskList service that accepts task ID
- [X] T027 [US3] Implement get_task_by_id method in TaskList service
- [X] T028 [US3] Implement CLI function to prompt user for task ID in src/todo_app/cli/main_menu.py
- [X] T029 [US3] Create CLI function to mark task complete/incomplete in src/todo_app/cli/main_menu.py
- [X] T030 [US3] Add error handling for invalid task IDs
- [X] T031 [US3] Display confirmation message after status change
- [X] T032 [US3] Update main menu to include "Mark Complete/Incomplete" option

---

## Phase 6: User Story 4 - Update Existing Task (Priority: P2)

### Goal
Allow users to modify the details of existing tasks by ID.

### Independent Test Criteria
- Task title and description can be updated by ID
- Error handling for invalid task IDs
- Confirmation message after update

### Acceptance Scenarios
1. Given user wants to update a task, When user runs update command with valid task ID and new details, Then system updates task information and displays confirmation
2. Given user provides invalid task ID, When user runs update command, Then system displays helpful error message

### Tasks

- [X] T033 [US4] Create update_task method in TaskList service that accepts task ID and new details
- [X] T034 [US4] Implement CLI function to get task ID for update in src/todo_app/cli/main_menu.py
- [X] T035 [US4] Implement CLI function to get new title for task in src/todo_app/cli/main_menu.py
- [X] T036 [US4] Implement CLI function to get new description for task in src/todo_app/cli/main_menu.py
- [X] T037 [US4] Create CLI function to update task details in src/todo_app/cli/main_menu.py
- [X] T038 [US4] Add validation for updated task data
- [X] T039 [US4] Add error handling for invalid task IDs
- [X] T040 [US4] Display confirmation message after update
- [X] T041 [US4] Update main menu to include "Update Task" option

---

## Phase 7: User Story 5 - Delete Task (Priority: P2)

### Goal
Allow users to remove tasks by ID.

### Independent Test Criteria
- Tasks can be removed by ID
- Error handling for invalid task IDs
- Confirmation message after deletion

### Acceptance Scenarios
1. Given user wants to remove a task, When user runs delete command with valid task ID, Then system removes task and displays confirmation
2. Given user provides invalid task ID, When user runs delete command, Then system displays helpful error message

### Tasks

- [X] T042 [US5] Create delete_task method in TaskList service that accepts task ID
- [X] T043 [US5] Implement CLI function to get task ID for deletion in src/todo_app/cli/main_menu.py
- [X] T044 [US5] Create CLI function to delete task in src/todo_app/cli/main_menu.py
- [X] T045 [US5] Add error handling for invalid task IDs
- [X] T046 [US5] Display confirmation message after deletion
- [X] T047 [US5] Update main menu to include "Delete Task" option

---

## Phase 8: Main Menu and Application Flow

### Goal
Implement the main menu loop and integrate all functionality.

### Independent Test Criteria
- Main menu presents all options clearly
- Menu loops continuously until user chooses to exit
- All user stories are accessible through the menu

### Tasks

- [X] T048 Implement main menu loop in src/main.py that continuously displays options
- [X] T049 Add "Exit" option to main menu
- [X] T050 Integrate all user story functions into main menu loop
- [X] T051 Add proper error handling for menu selection
- [X] T052 Handle application exit gracefully
- [X] T053 Ensure tasks are discarded when application exits

---

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Add finishing touches and handle cross-cutting concerns.

### Independent Test Criteria
- Application runs without errors
- All features work correctly
- Error handling is comprehensive
- User interface is clear and intuitive

### Tasks

- [X] T054 Add comprehensive error handling throughout the application
- [X] T055 Improve user interface with clear prompts and messages
- [X] T056 Add input sanitization and validation
- [X] T057 Add proper type hints to all functions
- [ ] T058 Create unit tests for all model and service functions
- [ ] T059 Create integration tests for CLI functionality
- [X] T060 Update README.md with usage instructions
- [X] T061 Run full application test to verify all functionality