---
id: 001
title: Implement GET Task Endpoint
stage: general
date: 2026-01-03
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: 001-fullstack-web-app
user: user
command: implement-get-task-endpoint
labels: ["backend", "api", "tasks", "endpoint", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/d/todo_phase1/backend/src/api/tasks.py
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py
tests:
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py::test_get_task_success
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py::test_get_task_unauthorized_access
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py::test_get_task_not_found
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py::test_get_task_missing_auth
---

## Prompt

Implement the GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py. The endpoint should:
- Retrieve a specific task for a user
- Validate that the requesting user has permission to access this task
- Validate that the task belongs to the specified user
- Return appropriate responses with proper HTTP status codes
- Handle errors properly (task not found, unauthorized access)
- Follow security best practices for user data isolation

## Response snapshot

I have successfully implemented the GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py with the following features:

1. Added a new endpoint function `get_task` that accepts user_id and task id as path parameters
2. Implemented proper validation to ensure the requesting user has permission to access the task
3. Added security validation to ensure the task belongs to the specified user
4. Included comprehensive error handling for:
   - 403 Forbidden when user doesn't have permission to access the task
   - 404 Not Found when the task doesn't exist
   - 500 Internal Server Error for unexpected errors
5. Added proper documentation with docstring explaining the endpoint functionality
6. Maintained consistency with existing code patterns and error handling approach
7. Added comprehensive tests for the new endpoint covering:
   - Successful task retrieval
   - Unauthorized access attempts
   - Non-existent task requests
   - Missing authentication

The endpoint is properly registered in main.py and follows all security best practices for user data isolation by checking both the user_id in the path matches the authenticated user and that the task belongs to that user.

## Outcome

- ✅ Impact: Implemented the required GET task endpoint with proper security validation
- 🧪 Tests: Added 4 comprehensive test cases for the new endpoint
- 📁 Files: Modified 2 files (tasks API and tests)
- 🔁 Next prompts: Ready for further API development or deployment
- 🧠 Reflection: Implementation follows existing patterns and security best practices

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A