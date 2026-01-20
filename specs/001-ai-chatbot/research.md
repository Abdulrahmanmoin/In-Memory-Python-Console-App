# Research: Todo AI Chatbot using MCP Server

## Decision: Technology Stack Selection
**Rationale**: The specification clearly defines the technology stack to be used:
- Backend: Python FastAPI
- AI: OpenAI Agents SDK
- MCP: Official MCP SDK
- ORM: SQLModel
- Database: Neon PostgreSQL
- Frontend: OpenAI ChatKit
- Authentication: Better Auth

This stack provides a solid foundation for the stateless, AI-powered todo chatbot with MCP tooling.

## Decision: System Architecture Pattern
**Rationale**: The architecture follows a clear separation of concerns:
- FastAPI handles API orchestration and conversation management
- OpenAI Agent performs natural language understanding and tool selection
- MCP Server exposes stateless tools for data operations
- PostgreSQL stores all persistent data
- Better Auth manages user authentication and scoping

## Decision: Data Model Design
**Rationale**: Based on the specification and clarifications, the data model includes:
- Conversation entity: id, user_id, created_at, updated_at
- Message entity: id, conversation_id, sender_type, content, timestamp
- Task entity: id, title (required), description (optional), completed (boolean, default false), created_at, updated_at, user_id

## Decision: MCP Tool Contract Design
**Rationale**: Five core tools are defined as per specification:
- add_task: Creates new task with title, description, user_id
- list_tasks: Returns all tasks for user_id
- complete_task: Updates task completion status
- update_task: Modifies task title/description
- delete_task: Removes task from database

Each tool validates user ownership and returns structured JSON responses.

## Decision: Stateless Operation Design
**Rationale**: The system maintains no in-memory session state between requests. Each API call:
1. Fetches complete conversation history from database
2. Appends new user message
3. Runs agent with MCP tools
4. Persists agent response and any tool effects
5. Returns response with conversation_id and tool calls

## Decision: Error Handling Strategy
**Rationale**: Following the clarification, errors are handled as:
- Validation errors return 400 with user-friendly messages
- System errors return 500 with generic messages
- AI interpretation errors return suggestions to user

## Decision: Authentication and Authorization
**Rationale**: Using Better Auth for user authentication with user_id scoping. All operations validate that users can only access their own data.

## Decision: Performance Requirements
**Rationale**: Based on clarifications, the system targets:
- API response time under 2 seconds for 95% of requests
- Support for up to 100 concurrent users

## Decision: Data Retention Policy
**Rationale**: User data (conversations, messages, tasks) retained indefinitely until user deletes their account or specific items.