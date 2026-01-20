# Quickstart Guide: Todo AI Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL (or Neon Serverless PostgreSQL)
- Better Auth account
- OpenAI API key
- OpenAI MCP server setup

## Environment Setup

1. Clone the repository:
```bash
git clone <repo-url>
cd todo-ai-chatbot
```

2. Set up backend environment:
```bash
cd backend
cp .env.example .env
# Edit .env with your configuration
```

3. Set up frontend environment:
```bash
cd ../frontend
cp .env.example .env
# Edit .env with your configuration
```

## Backend Setup

1. Install Python dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set environment variables in `.env`:
```bash
# Database
DATABASE_URL="postgresql://..."

# Authentication
BETTER_AUTH_SECRET="your-secret-key"
BETTER_AUTH_URL="http://localhost:3000"

# OpenAI
OPENAI_API_KEY="sk-..."

# MCP Server
MCP_SERVER_URL="http://localhost:8000"
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the backend:
```bash
uvicorn src.main:app --reload --port 8000
```

## MCP Server Setup

1. Navigate to the MCP server directory:
```bash
cd backend/src/mcp_server
```

2. Start the MCP server:
```bash
python tools.py
```

## Frontend Setup

1. Install Node.js dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Configuration

The system requires the following configurations:

- **Database**: Neon Serverless PostgreSQL with SQLModel
- **Authentication**: Better Auth with JWT tokens
- **AI Agent**: OpenAI Agents SDK with tools attached
- **MCP Server**: Official MCP SDK with task management tools

## Running the Application

1. Start the MCP server: `python backend/src/mcp_server/tools.py`
2. Start the backend API: `uvicorn backend/src/main.py:app --port 8000`
3. Start the frontend: `npm run dev` in the frontend directory
4. Access the application at `http://localhost:3000`

## Testing the Chat Functionality

1. Authenticate with Better Auth
2. Navigate to the chat interface
3. Send a message like "add buy groceries to my list"
4. The AI assistant should respond and create the task
5. Verify the task appears in your task list

## Troubleshooting

- Ensure all services are running (MCP server, backend API, frontend)
- Check that environment variables are properly set
- Verify database connectivity
- Confirm API keys are valid and have necessary permissions