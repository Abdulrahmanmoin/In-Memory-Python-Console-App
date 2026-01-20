# Feature Specification: Todo AI Chatbot using MCP Server

**Feature Branch**: `001-ai-chatbot`
**Created**: 2026-01-17
**Status**: Draft
**Input**: User description: "Phase III – Todo AI Chatbot using MCP Server

Objective:
Design and implement a basic-level AI-powered Todo chatbot that allows users to manage tasks through natural language. The system must use a stateless FastAPI backend, OpenAI Agents SDK for reasoning, and an MCP (Model Context Protocol) server that exposes task operations as tools. All conversation and task state must be persisted in a PostgreSQL database.

Core capabilities:
- Conversational task creation, listing, updating, completion, and deletion
- Natural language understanding mapped to explicit MCP tool calls
- Stateless chat endpoint that reconstructs context from database
- MCP tools that are stateless and operate only via persisted data
- Conversation continuity across requests and server restarts

Success criteria:
- User can fully manage todos using natural language commands
- Agent correctly selects and invokes MCP tools based on user intent
- All chat requests are stateless (no in-memory session state)
- Conversation history is persisted and correctly replayed to the agent
- MCP tool invocations are recorded and returned in API responses
- Errors (task not found, invalid input) are handled gracefully
- System resumes conversations after server restart without loss of context

Functional scope (building):
1. Chat API
   - POST /api/{user_id}/chat endpoint
   - Accepts user message and optional conversation_id
   - Creates new conversation if conversation_id is missing
   - Stores user and assistant messages in database
   - Returns assistant response, conversation_id, and MCP tool calls

2. AI Agent
   - Built using OpenAI Agents SDK
   - Receives full conversation history from database
   - Uses MCP tools exclusively for task operations
   - Never modifies state directly (no DB access outside MCP tools)
   - Confirms all actions with friendly, human-readable responses

3. MCP Server
   - Implemented using the Official MCP SDK
   - Exposes stateless tools:
     - add_task
     - list_tasks
     - complete_task
     - update_task
     - delete_task
   - Tools persist state using SQLModel + PostgreSQL
   - Tools return structured outputs suitable for agent consumption

4. Database Layer
   - Neon Serverless PostgreSQL
   - SQLModel ORM
   - Models:
     - Conversation (chat sessions)
     - Message (chat history)

5. Authentication
   - Better Auth
   - All operations scoped by user_id

Agent behavior rules:
- Add task when user intent implies creation (add, remember, create)
- List tasks when user asks to see, show, or query tasks
- Complete task when user says done, complete, finished
- Delete task when user says delete, remove, cancel
- Update task when user says change, rename, update
- If task reference is ambiguous, list tasks first before acting
- Always confirm actions in plain, friendly language
- Handle missing or invalid task IDs without crashing

Conversation lifecycle (stateless request cycle):
1. Receive user message
2. Fetch conversation + message history from database
3. Append new user message
4. Run OpenAI Agent with MCP tools enabled
5. Agent invokes one or more MCP tools
6. Persist tool effects and assistant response
7. Return response to client
8. Server retains no in-memory state

Technology constraints:
- Backend: Python FastAPI
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK only
- ORM: SQLModel
- Database: Neon PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

API contract constraints:
- POST /api/{user_id}/chat
- Request fields:
  - message (string, required)
  - conversation_id (integer, optional)
- Response fields:
  - conversation_id (integer)
  - response (string)
  - tool_calls (array)

MCP tool constraints:
- Tools must be stateless
- Tools must validate user_id ownership
- Tools must return structured JSON responses
- Tools must not contain business logic beyond their scope

Deliverables:
- GitHub repository containing:
  - /frontend – ChatKit UI
  - /backend – FastAPI + OpenAI Agents SDK + MCP Server
  - /specs – Agent and MCP tool specifications
  - Database migration scripts
  - README with setup and run instructions

Non-goals (not building):
- Voice input or speech-to-text
- Task prioritization or reminders
- Multi-user shared task lists
- Real-time streaming responses
- Advanced AI planning or long-term memory
- Mobile application

Quality bar:
- Clear separation of concerns (UI, Agent, MCP, DB)
- Deterministic tool behavior
- Predictable agent actions
- Easy extensibility for future phases
- Specs readable by humans and executable by AI agents"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Language Todo Management (Priority: P1)

A user wants to manage their tasks through natural conversation with an AI assistant. They can say things like "add buy groceries" or "show me my tasks" and the system will interpret their intent and perform the appropriate action. The user can create, view, update, complete, and delete tasks using natural language commands.

**Why this priority**: This is the core value proposition of the feature - allowing users to manage tasks through natural conversation rather than structured interfaces.

**Independent Test**: The system can accept natural language commands and translate them to appropriate task operations, returning friendly responses that confirm actions taken.

**Acceptance Scenarios**:

1. **Given** user is authenticated and has access to the chat interface, **When** user sends "add buy milk and bread to my grocery list", **Then** system creates a new task with title "buy milk and bread to my grocery list" and returns a confirmation message

2. **Given** user has multiple tasks in their list, **When** user sends "show me my tasks", **Then** system retrieves and displays all user's tasks in a readable format

3. **Given** user has an existing task, **When** user sends "complete task 1", **Then** system marks the specified task as completed and confirms the action

4. **Given** user has multiple tasks, **When** user sends "update task 2 to say buy organic milk", **Then** system updates the specified task and confirms the change

5. **Given** user has completed tasks, **When** user sends "delete task 3", **Then** system removes the specified task and confirms deletion

---

### User Story 2 - Persistent Conversation Context (Priority: P2)

A user wants to continue their conversation with the AI assistant across multiple sessions. When they return to the chat, the system remembers their previous conversation and can continue from where they left off, maintaining context about their tasks and preferences.

**Why this priority**: Essential for a good user experience - users expect conversations to be persistent and context-aware across sessions.

**Independent Test**: The system can reconstruct conversation history from the database and continue conversations seamlessly after server restarts or user disconnections.

**Acceptance Scenarios**:

1. **Given** user has an ongoing conversation with task context, **When** server restarts and user reconnects, **Then** system restores the conversation state and can continue from where it left off

2. **Given** user has multiple conversation threads, **When** user specifies a conversation ID, **Then** system loads the specific conversation history and continues appropriately

3. **Given** user is in middle of a multi-step task operation, **When** network interruption occurs, **Then** user can resume the conversation and complete the operation

---

### User Story 3 - MCP Tool Integration (Priority: P3)

An AI agent needs to interact with the system through standardized tools exposed via the Model Context Protocol (MCP) server. The agent receives conversation history and uses specific tools to manipulate tasks rather than having direct database access.

**Why this priority**: Enables clean separation of concerns between AI reasoning and data operations, making the system more maintainable and secure.

**Independent Test**: The MCP server exposes stateless tools that can be invoked by the AI agent to perform task operations with proper user authentication and validation.

**Acceptance Scenarios**:

1. **Given** AI agent needs to create a task, **When** agent invokes the add_task tool with proper parameters, **Then** system creates the task and returns success confirmation

2. **Given** AI agent needs to list tasks, **When** agent invokes the list_tasks tool, **Then** system returns the user's tasks in structured format

3. **Given** AI agent needs to update a task, **When** agent invokes the update_task tool with valid parameters, **Then** system updates the task and returns confirmation

---

### Edge Cases

- What happens when a user tries to access tasks belonging to another user? The system should validate user ownership and reject unauthorized access.
- How does the system handle invalid task IDs or malformed requests? The system should return appropriate error messages without exposing internal details.
- What happens when a user asks to perform an action on a task that doesn't exist? The system should gracefully handle the error and suggest alternatives.
- How does the system respond when the AI agent makes multiple rapid tool calls? The system should process them sequentially without conflicts.
- What happens when conversation history becomes very long? The system should manage memory efficiently while maintaining context.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a chat API endpoint at POST /api/{user_id}/chat that accepts user messages and optional conversation_id
- **FR-002**: System MUST persist all conversation messages in a PostgreSQL database with proper user scoping
- **FR-003**: System MUST reconstruct full conversation history from database before processing each new message
- **FR-004**: System MUST integrate with OpenAI Agents SDK to process natural language and invoke appropriate tools
- **FR-005**: System MUST expose MCP tools for add_task, list_tasks, complete_task, update_task, and delete_task operations
- **FR-006**: System MUST validate that all operations are scoped to the authenticated user_id
- **FR-007**: System MUST return structured responses including conversation_id, response text, and tool call records
- **FR-008**: System MUST handle natural language interpretation for task creation (add, remember, create), listing (show, see, query), completion (done, complete, finished), deletion (delete, remove, cancel), and updates (change, rename, update)
- **FR-009**: System MUST provide friendly, human-readable confirmation messages for all actions performed
- **FR-010**: System MUST handle ambiguous task references by listing available tasks before performing actions
- **FR-011**: System MUST gracefully handle missing or invalid task IDs without crashing
- **FR-012**: System MUST be stateless - no in-memory session state retained between requests
- **FR-013**: System MUST support conversation continuity across server restarts by relying solely on database persistence

### Key Entities *(include if feature involves data)*

- **Conversation**: Represents a chat session between user and AI assistant, contains metadata like creation time, last activity, and user association
- **Message**: Represents a single message in a conversation, includes sender type (user/assistant), content, timestamp, and associated conversation
- **Task**: Represents a user's todo item with specific attributes: id (unique identifier), title (string, required), description (string, optional), completed (boolean, default false), created_at (timestamp), updated_at (timestamp), user_id (foreign key for user ownership)

## Clarifications

### Session 2026-01-17

- Q: What are the specific attributes for the Task entity? → A: Task should have id, title (string, required), description (string, optional), completed (boolean, default false), created_at (timestamp), updated_at (timestamp), user_id (foreign key)
- Q: What are the specific performance requirements for the chat API and system responsiveness? → A: API response time should be under 2 seconds for 95% of requests, and system should handle up to 100 concurrent users
- Q: What specific security and privacy measures should be implemented? → A: Basic authentication only, no additional security measures
- Q: How should the system specifically handle different types of errors? → A: Validation errors return 400 with user-friendly messages, system errors return 500 with generic messages, AI interpretation errors return suggestions to user
- Q: Should there be any specific data retention policies for conversations, messages, or tasks? → A: User data (conversations, messages, tasks) should be retained indefinitely until user deletes their account or specific items

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can fully manage their todos using natural language commands with 95% accuracy in intent recognition
- **SC-002**: AI agent correctly selects and invokes appropriate MCP tools based on user intent in 90% of interactions
- **SC-003**: All chat requests are processed statelessly with no in-memory session data retained between requests
- **SC-004**: Conversation history is completely reconstructed from database and accurately replayed to the agent for each request
- **SC-005**: MCP tool invocations are properly recorded and returned in API responses 100% of the time
- **SC-006**: System handles error cases (task not found, invalid input) gracefully with user-friendly error messages 100% of the time
- **SC-007**: Conversations resume correctly after server restarts without loss of context 100% of the time
- **SC-008**: System maintains conversation context across multiple requests with consistent user experience
