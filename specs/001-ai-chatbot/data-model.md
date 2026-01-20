# Data Model: Todo AI Chatbot

## Entity Relationships

```
Conversation (1) ←→ (Many) Message
Conversation (1) ←→ (Many) Task
User (1) ←→ (Many) Conversation
```

## Entity Definitions

### Conversation
Represents a chat session between user and AI assistant

- `id`: Integer (Primary Key, Auto-generated)
- `user_id`: String (Foreign Key, references user identity from auth)
- `created_at`: DateTime (Timestamp when conversation started)
- `updated_at`: DateTime (Timestamp of last activity)

### Message
Represents a single message in a conversation

- `id`: Integer (Primary Key, Auto-generated)
- `conversation_id`: Integer (Foreign Key, references Conversation.id)
- `sender_type`: String (Enum: "user" | "assistant")
- `content`: Text (The actual message content)
- `timestamp`: DateTime (When the message was sent)

### Task
Represents a user's todo item

- `id`: Integer (Primary Key, Auto-generated)
- `title`: String (Required, max 255 characters)
- `description`: Text (Optional, longer description)
- `completed`: Boolean (Default: False)
- `user_id`: String (Foreign Key, references user identity from auth)
- `created_at`: DateTime (Timestamp when task was created)
- `updated_at`: DateTime (Timestamp of last update)

## Indexes

- Conversation.user_id (for user-specific queries)
- Message.conversation_id (for conversation history retrieval)
- Task.user_id (for user-specific task queries)
- Task.completed (for filtering completed tasks)

## Constraints

- All entities must have user_id for proper scoping
- Task.title is required (not nullable)
- Task.completed defaults to False
- Foreign key constraints enforce referential integrity
- All timestamps are in UTC