# Implementation Tasks: Todo AI Chatbot using MCP Server

**Feature**: Todo AI Chatbot using MCP Server
**Branch**: `001-ai-chatbot`
**Created**: 2026-01-17
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Implementation Strategy

Implement the Todo AI Chatbot in phases following the user story priorities:
- **Phase 1 (Setup)**: Project structure and foundational components
- **Phase 2 (Foundational)**: Database models and authentication setup
- **Phase 3 (US1)**: Natural Language Todo Management (P1 priority)
- **Phase 4 (US2)**: Persistent Conversation Context (P2 priority)
- **Phase 5 (US3)**: MCP Tool Integration (P3 priority)
- **Phase 6 (Polish)**: Cross-cutting concerns and validation

The MVP will include basic chat functionality with task creation and management (US1), with subsequent phases adding persistence and MCP integration.

## Phase 1: Setup

**Goal**: Initialize project structure and foundational components

- [ ] T001 Create backend directory structure with src/models, src/services, src/api, src/mcp_server
- [ ] T002 Create frontend directory structure with src/components, src/pages, src/services, src/types
- [ ] T003 Set up backend requirements.txt with FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon PostgreSQL, Better Auth
- [ ] T004 Set up backend pyproject.toml with proper configuration
- [ ] T005 Create backend alembic directory structure
- [ ] T006 Set up frontend package.json with Next.js and OpenAI ChatKit dependencies
- [ ] T007 Create basic backend main.py with FastAPI app initialization
- [ ] T008 Create basic frontend pages/_app.js and pages/index.js

## Phase 2: Foundational

**Goal**: Set up database models, authentication, and core services

- [ ] T009 [P] Create Task model in backend/src/models/task.py with id, title, description, completed, user_id, created_at, updated_at
- [ ] T010 [P] Create Conversation model in backend/src/models/conversation.py with id, user_id, created_at, updated_at
- [ ] T011 [P] Create Message model in backend/src/models/message.py with id, conversation_id, sender_type, content, timestamp
- [ ] T012 Create database service in backend/src/services/database.py with connection and session management
- [ ] T013 Set up Better Auth integration in backend/src/services/auth.py
- [ ] T014 [P] Create Alembic migration files for Task, Conversation, and Message models

## Phase 3: [US1] Natural Language Todo Management

**Goal**: Enable users to manage tasks through natural conversation with AI assistant

**Independent Test**: The system can accept natural language commands and translate them to appropriate task operations, returning friendly responses that confirm actions taken.

- [ ] T015 Create MCP server tools in backend/src/mcp_server/tools.py with add_task, list_tasks, complete_task, update_task, delete_task
- [ ] T016 [P] [US1] Implement add_task function in MCP tools with title, description, user_id validation
- [ ] T017 [P] [US1] Implement list_tasks function in MCP tools with user_id scoping
- [ ] T018 [P] [US1] Implement complete_task function in MCP tools with user validation
- [ ] T019 [P] [US1] Implement update_task function in MCP tools with user validation
- [ ] T020 [P] [US1] Implement delete_task function in MCP tools with user validation
- [ ] T021 Create agent service in backend/src/services/agent.py with OpenAI Agent SDK integration
- [ ] T022 [P] [US1] Configure OpenAI Agent with MCP tools attachment
- [ ] T023 [P] [US1] Implement intent detection for task creation (add, remember, create)
- [ ] T024 [P] [US1] Implement intent detection for task listing (show, see, query)
- [ ] T025 [P] [US1] Implement intent detection for task completion (done, complete, finished)
- [ ] T026 [P] [US1] Implement intent detection for task deletion (delete, remove, cancel)
- [ ] T027 [P] [US1] Implement intent detection for task updates (change, rename, update)
- [ ] T028 [US1] Create chat API endpoint in backend/src/api/chat.py with POST /api/{user_id}/chat
- [ ] T029 [P] [US1] Implement request validation for chat endpoint (message required, conversation_id optional)
- [ ] T030 [P] [US1] Implement conversation creation logic when conversation_id is missing
- [ ] T031 [P] [US1] Implement message persistence for user messages
- [ ] T032 [P] [US1] Implement conversation history reconstruction
- [ ] T033 [P] [US1] Implement agent execution with MCP tools enabled
- [ ] T034 [P] [US1] Implement assistant response persistence
- [ ] T035 [P] [US1] Implement response formatting with conversation_id, response text, and tool calls
- [ ] T036 [P] [US1] Implement error handling for task not found scenarios
- [ ] T037 [P] [US1] Implement error handling for invalid input scenarios
- [ ] T038 [US1] Create basic frontend chat interface in frontend/src/pages/chat.js
- [ ] T039 [P] [US1] Implement chat UI with message display and input field
- [ ] T040 [P] [US1] Connect frontend to backend chat API
- [ ] T041 [P] [US1] Implement response display showing assistant messages and tool calls

## Phase 4: [US2] Persistent Conversation Context

**Goal**: Enable users to continue conversations across multiple sessions with preserved context

**Independent Test**: The system can reconstruct conversation history from the database and continue conversations seamlessly after server restarts or user disconnections.

- [ ] T042 [P] [US2] Enhance conversation model to track last activity properly
- [ ] T043 [P] [US2] Implement conversation history retrieval with proper ordering
- [ ] T044 [P] [US2] Optimize message retrieval for long conversations
- [ ] T045 [P] [US2] Implement conversation context preservation across server restarts
- [ ] T046 [P] [US2] Add conversation_id persistence in frontend
- [ ] T047 [P] [US2] Implement conversation switching functionality in UI
- [ ] T048 [P] [US2] Add conversation history display in UI
- [ ] T049 [US2] Test conversation continuity after simulated server restart

## Phase 5: [US3] MCP Tool Integration

**Goal**: Ensure MCP server exposes stateless tools that can be invoked by AI agent with proper validation

**Independent Test**: The MCP server exposes stateless tools that can be invoked by the AI agent to perform task operations with proper user authentication and validation.

- [ ] T050 [P] [US3] Implement proper user_id validation in all MCP tools
- [ ] T051 [P] [US3] Add ownership validation to prevent cross-user access
- [ ] T052 [P] [US3] Implement structured JSON responses for all MCP tools
- [ ] T053 [P] [US3] Add logging for MCP tool invocations
- [ ] T054 [P] [US3] Implement tool call recording in chat API responses
- [ ] T055 [P] [US3] Add rate limiting to MCP tools if needed
- [ ] T056 [US3] Test MCP tool integration with AI agent
- [ ] T057 [US3] Validate stateless operation of MCP tools

## Phase 6: Polish & Cross-Cutting Concerns

**Goal**: Address cross-cutting concerns and finalize implementation

- [ ] T058 Add comprehensive error handling throughout the system
- [ ] T059 Implement proper logging for debugging and monitoring
- [ ] T060 Add input validation and sanitization
- [ ] T061 Implement proper exception handling with user-friendly messages
- [ ] T062 Add performance optimizations for large conversation histories
- [ ] T063 Write comprehensive API documentation
- [ ] T064 Create README.md files for both backend and frontend
- [ ] T065 Set up environment configuration for different deployment stages
- [ ] T066 Implement health check endpoints
- [ ] T067 Add tests for critical functionality
- [ ] T068 Conduct end-to-end testing of all user stories
- [ ] T069 Validate all success criteria from the specification

## Dependencies

- User Story 1 (Natural Language Todo Management) must be completed before User Story 2 and 3 can be fully validated
- Foundational phase (database models, auth) must be completed before any user story phases
- MCP server tools (Phase 5) should be stable before full AI agent integration (Phase 3)

## Parallel Execution Examples

- Tasks T009-T011 (models) can be developed in parallel
- Tasks T016-T020 (MCP tools) can be developed in parallel
- Tasks T023-T027 (intent detection) can be developed in parallel
- Tasks T038-T041 (frontend) can be developed in parallel with backend API implementation