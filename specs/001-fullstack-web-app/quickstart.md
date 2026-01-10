# Quickstart Guide: Full-Stack Web Application

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL (or Neon Serverless PostgreSQL account)
- pnpm or npm (for frontend package management)

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <repository-url>
cd <repository-name>

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
# or
pnpm install
```

### 2. Environment Configuration

Create `.env` files in both backend and frontend directories:

**Backend (.env):**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days in minutes
BETTER_AUTH_SECRET=your-better-auth-secret
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

### 3. Database Setup

```bash
# From backend directory
cd backend

# Run database migrations
python -m src.database.connection --migrate

# Or if using SQLModel directly
python -c "from src.database.connection import engine; from src.models.user import User; from src.models.task import Task; User.metadata.create_all(engine); Task.metadata.create_all(engine)"
```

### 4. Running the Application

#### Backend (FastAPI)
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

#### Frontend (Next.js)
```bash
cd frontend
npm run dev
# or
pnpm dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend API Docs: http://localhost:8000/docs

## API Endpoints

### Authentication Endpoints
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout

### Task Endpoints
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Development Workflow

### Backend Development
1. Make changes to Python files in `backend/src/`
2. Server automatically reloads due to `--reload` flag
3. API documentation updates automatically at `/docs`

### Frontend Development
1. Make changes to TypeScript/JSX files in `frontend/src/`
2. Development server automatically reloads
3. Hot Module Replacement updates components without full page reload

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
# or
pnpm test
```

## Deployment Notes

### Environment Variables for Production
- Update DATABASE_URL to production database
- Use strong SECRET_KEY and BETTER_AUTH_SECRET
- Set NEXT_PUBLIC_API_URL to production backend URL
- Configure proper CORS settings for production domains

### Database Migration in Production
- Run migrations before deploying new versions that include schema changes
- Backup database before running migrations in production