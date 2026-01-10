---
id: 002
title: Implement PUT task endpoint
stage: tasks
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fullstack-web-app
branch: 001-fullstack-web-app
user: claude-code
command: implement-put-task-endpoint
labels: [api, tasks, endpoint, update]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - /mnt/d/todo_phase1/backend/src/api/tasks.py
tests:
  - /mnt/d/todo_phase1/backend/tests/test_tasks.py
---

## Prompt

Implement the PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/tasks.py. The endpoint should:
- Update a specific task for a user
- Validate that the requesting user has permission to update this task
- Validate that the task belongs to the specified user
- Validate input data using appropriate models
- Return appropriate responses with proper HTTP status codes
- Handle errors properly (task not found, unauthorized access)
- Follow security best practices

## Response snapshot

I have successfully implemented the PUT /api/{user_id}/tasks/{id} endpoint in the backend. Here's what was added to the tasks API file:

1. Added a new `@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)` endpoint
2. The endpoint accepts user_id (UUID), task id (UUID), and task_data (TaskUpdate)
3. It validates that the current user has permission to update the task by checking user_id
4. It verifies the task exists and belongs to the specified user
5. It updates the task fields with the provided data, handling completion status appropriately
6. It updates the `updated_at` timestamp and handles `completed_at` based on completion status
7. It includes comprehensive error handling with appropriate HTTP status codes:
   - 403 Forbidden if user doesn't have permission
   - 404 Not Found if task doesn't exist
   - 500 Internal Server Error for database errors
8. Added detailed docstring explaining the endpoint functionality

The implementation follows security best practices by ensuring data isolation between users and validating permissions at multiple levels.

## Outcome

- ✅ Impact: Successfully implemented the PUT endpoint for updating tasks with proper authentication and authorization
- 🧪 Tests: Need to add tests for the new endpoint
- 📁 Files: Modified /mnt/d/todo_phase1/backend/src/api/tasks.py to add the endpoint
- 🔁 Next prompts: Add tests for the new endpoint, potentially add validation for title length
- 🧠 Reflection: The implementation follows the same security patterns as other endpoints in the file

## Evaluation notes (flywheel)

- Failure modes observed: None observed during implementation
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add integration tests for the new endpoint