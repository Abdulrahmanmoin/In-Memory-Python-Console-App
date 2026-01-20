---
id: 2
title: "todo-ai-chatbot-planning"
stage: "plan"
date_iso: "2026-01-17"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "001-ai-chatbot"
branch: "001-ai-chatbot"
user: "user"
command: "/sp.plan Organize work by phases:\nPhase 1 – Architecture & Foundations\nPhase 2 – MCP Server & Tooling\nPhase 3 – AI Agent Integration\nPhase 4 – Chat API & Conversation Lifecycle\nPhase 5 – Frontend Integration\nPhase 6 – Validation, Testing, and Hardening"
labels: ["planning", "architecture", "ai", "mcp", "todo"]
links:
  spec: "specs/001-ai-chatbot/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - specs/001-ai-chatbot/plan.md
  - specs/001-ai-chatbot/research.md
  - specs/001-ai-chatbot/data-model.md
  - specs/001-ai-chatbot/contracts/chat-api.yaml
  - specs/001-ai-chatbot/quickstart.md
tests_yaml: |
  - "Architecture verification"
  - "Data model validation"
  - "API contract review"
  - "Quickstart guide validation"
---

# PHR: todo-ai-chatbot-planning

## Original Prompt

Organize work by phases:
Phase 1 – Architecture & Foundations
Phase 2 – MCP Server & Tooling
Phase 3 – AI Agent Integration
Phase 4 – Chat API & Conversation Lifecycle
Phase 5 – Frontend Integration
Phase 6 – Validation, Testing, and Hardening

------------------------------------
Phase 1 – Architecture & Foundations
------------------------------------
- Finalize system boundaries and data flow:
  - ChatKit UI → FastAPI → OpenAI Agent SDK → MCP Server → PostgreSQL
- Define stateless contract for:
  - Chat endpoint
  - MCP tools
- Define ownership rules:
  - Agent performs reasoning only
  - MCP tools mutate state
  - FastAPI orchestrates only
- Establish authentication and user scoping model
- Define error handling strategy (task not found, invalid input)
- Produce architecture diagram and responsibility matrix

Decisions needing documentation:
- Where conversation context is reconstructed (API vs Agent runner)
- How tool calls are logged and returned
- How ambiguous user intent is resolved
Tradeoffs:
- Simpler agent logic vs. richer intent disambiguation
- Fewer MCP tools vs. clearer, single-purpose tools

------------------------------------
Phase 2 – MCP Server & Tooling
------------------------------------
- Design MCP server using Official MCP SDK
- Define each MCP tool contract:
  - add_task
  - list_tasks
  - complete_task
  - update_task
  - delete_task
- Define input validation and ownership checks
- Map tools directly to SQLModel operations
- Ensure tools are fully stateless and database-backed
- Document example inputs/outputs for each tool

Decisions needing documentation:
- Tool granularity (single update tool vs multiple)
- Error response shape (null vs structured error)
Tradeoffs:
- Simpler tool API vs. richer feedback to agent

------------------------------------
Phase 3 – AI Agent Integration
------------------------------------
- Define agent role and responsibilities
- Configure OpenAI Agents SDK runner
- Attach MCP tools to agent
- Define agent behavior rules:
  - Intent → Tool mapping
  - Confirmation responses
  - Multi-step actions (e.g., list then delete)
- Define system prompt and guardrails
- Ensure agent never directly accesses database

Decisions needing documentation:
- How much reasoning is exposed to user
- How agent handles partial or unclear instructions
Tradeoffs:
- Deterministic behavior vs. flexible language handling

------------------------------------
Phase 4 – Chat API & Conversation Lifecycle
------------------------------------
- Implement POST /api/{user_id}/chat flow:
  - Fetch conversation history
  - Append new user message
  - Run agent
  - Persist assistant response
- Define conversation creation logic
- Define message storage strategy
- Ensure server remains stateless between requests
- Return tool call metadata to client

Decisions needing documentation:
- Message history length limits
- Ordering and replay strategy
Tradeoffs:
- Full history replay vs. truncated context window

------------------------------------
Phase 5 – Frontend Integration
------------------------------------
- Integrate OpenAI ChatKit UI
- Connect chat UI to backend API
- Display assistant responses and confirmations
- Handle loading, errors, and retries
- Ensure conversation_id persistence on client side

Decisions needing documentation:
- Client-side conversation storage
- Error display strategy
Tradeoffs:
- Simplicity vs. richer UX feedback

------------------------------------
Phase 6 – Validation, Testing, and Hardening
------------------------------------
Testing strategy:
- Unit tests for MCP tools (DB state changes)
- Agent behavior tests with predefined prompts
- API integration tests (stateless behavior)
- Conversation continuity tests across requests
- Error handling and edge case validation

Validation checks (acceptance-criteria based):
- Can user manage tasks via natural language only
- Does agent invoke correct MCP tools
- Does server remain stateless across requests
- Are conversations resumable after restart
- Are tool calls correctly logged and returned
- Are all errors handled gracefully

Quality bar:
- Clear separation of concerns
- Predictable agent behavior
- Deterministic MCP tool execution
- Easy extensibility for future phases

Deliverables:
- Architecture documentation
- MCP tool specs
- Agent behavior spec
- API flow documentation
- Test plan and validation checklist

## Response Summary

Successfully completed the implementation planning for the Todo AI Chatbot using MCP Server. The planning included:

- Technical Context: Defined the technology stack (Python 3.11, FastAPI, OpenAI Agents SDK, MCP SDK, SQLModel, Neon PostgreSQL, Better Auth, OpenAI ChatKit)
- Constitution Check: Verified all constitutional requirements are met
- Project Structure: Outlined the web application architecture with separate backend and frontend directories
- Research: Created comprehensive research document covering all technical decisions
- Data Model: Defined the entities (Conversation, Message, Task) and their relationships
- API Contracts: Documented the chat API and MCP tool contracts
- Quickstart Guide: Provided setup and configuration instructions

All deliverables mentioned in the original requirements have been created and the architecture follows the required separation of concerns between the UI, API, AI agent, and MCP server components.

## Outcome

Planning phase complete with all required artifacts created:
- Implementation plan at specs/001-ai-chatbot/plan.md
- Research document at specs/001-ai-chatbot/research.md
- Data model at specs/001-ai-chatbot/data-model.md
- API contracts at specs/001-ai-chatbot/contracts/chat-api.yaml
- Quickstart guide at specs/001-ai-chatbot/quickstart.md
- Agent context updated in CLAUDE.md