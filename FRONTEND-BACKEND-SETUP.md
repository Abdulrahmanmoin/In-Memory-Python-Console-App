# Frontend-Backend Integration Setup Guide

This guide explains how to properly configure the frontend and backend for both local development and Docker deployment.

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Port Configuration](#port-configuration)
- [Local Development Setup](#local-development-setup)
- [Docker Deployment Setup](#docker-deployment-setup)
- [API Endpoints](#api-endpoints)
- [Troubleshooting](#troubleshooting)

## Architecture Overview

The application consists of:
- **Frontend**: Next.js application (Port 3000)
- **Backend**: FastAPI application (Port 8000)
- **Database**: Neon Serverless PostgreSQL

## Port Configuration

### Backend Ports
- **Local Development**: `http://localhost:8000`
- **Docker**: `http://backend:8000` (internal) / `http://localhost:8000` (external)

### Frontend Ports
- **Local Development**: `http://localhost:3000`
- **Docker**: `http://frontend:3000` (internal) / `http://localhost:3000` (external)

## Local Development Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your configuration:
   ```env
   PORT=8000
   HOST=0.0.0.0
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/todo_db
   JWT_SECRET_KEY=your-secret-key-here
   ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
   ```

4. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   python -m src.main
   ```

   The backend will start on `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Create a `.env.local` file for local development:
   ```bash
   cp .env.local.example .env.local
   ```

3. Update the `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   BETTER_AUTH_SECRET=your-secret-here
   BETTER_AUTH_URL=http://localhost:3000
   ```

4. Install dependencies and run:
   ```bash
   npm install
   npm run dev
   ```

   The frontend will start on `http://localhost:3000`

## Docker Deployment Setup

### Prerequisites
- Docker and Docker Compose installed
- Environment variables configured

### Environment Configuration

1. **Backend**: Uses the `.env` file in the `backend/` directory
   - Already configured for Docker with PORT=8000

2. **Frontend**: Uses the `.env` file in the `frontend/` directory
   ```env
   NEXT_PUBLIC_API_URL=http://backend:8000
   ```

   Note: Use the service name `backend` (not `todo-backend` or `localhost`)

### Running with Docker Compose

1. Build and start all services:
   ```bash
   docker-compose up --build
   ```

2. Access the application:
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

3. Stop the services:
   ```bash
   docker-compose down
   ```

## API Endpoints

The backend provides the following main endpoints:

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user
- `GET /api/v1/auth/me` - Get current user

### Tasks
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

### Health Check
- `GET /health` - Health check endpoint

## Frontend API Integration

The frontend uses a centralized API utility (`src/lib/api.ts`) that:

1. Reads `NEXT_PUBLIC_API_URL` from environment variables
2. Automatically adds authentication headers (JWT token from localStorage)
3. Handles errors consistently
4. Provides typed request/response handling

### Example Usage

```typescript
import { api } from '@/lib/api';

// Get all tasks
const tasks = await api.get<Task[]>(`/api/${userId}/tasks`);

// Create a task
const newTask = await api.post<CreateTaskRequest, Task>(
  `/api/${userId}/tasks`,
  { title: 'New Task', description: 'Description' }
);

// Update a task
const updatedTask = await api.put<UpdateTaskRequest, Task>(
  `/api/${userId}/tasks/${taskId}`,
  { title: 'Updated Title' }
);

// Delete a task
await api.delete(`/api/${userId}/tasks/${taskId}`);
```

## Troubleshooting

### Issue: Frontend can't connect to backend

**Symptom**: Network errors or timeout when calling API

**Solutions**:

1. **Local Development**:
   - Ensure backend is running on port 8000
   - Check `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
   - Verify CORS settings in backend allow `http://localhost:3000`

2. **Docker**:
   - Ensure frontend `.env` uses `http://backend:8000` (not `localhost`)
   - Verify both containers are on the same network
   - Check docker-compose.yml network configuration

### Issue: CORS errors

**Symptom**: Browser shows CORS policy errors

**Solution**:
- Add your frontend URL to `ALLOWED_ORIGINS` in backend `.env`
- Format: `ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000`

### Issue: Authentication not working

**Symptom**: 401 Unauthorized errors

**Solution**:
- Check JWT_SECRET_KEY is set in backend `.env`
- Verify token is being stored in localStorage
- Check Authorization header is being sent with requests

### Issue: Port already in use

**Symptom**: Can't start service due to port conflict

**Solution**:
- Stop other services using the port
- Change port in configuration files
- For backend: Update `PORT` in `.env`
- For frontend: Use `PORT=3001 npm run dev`

### Issue: Database connection fails

**Symptom**: Backend can't connect to database

**Solution**:
- Verify `DATABASE_URL` in backend `.env` is correct
- For Neon: Check connection string includes `?sslmode=require`
- Test database connectivity separately

## Configuration Files Reference

### Backend Files
- `backend/.env` - Main environment configuration
- `backend/.env.example` - Template for environment variables
- `backend/src/config.py` - Settings class that reads environment variables
- `backend/src/main.py` - FastAPI application entry point

### Frontend Files
- `frontend/.env` - Docker environment configuration
- `frontend/.env.local` - Local development configuration (gitignored)
- `frontend/.env.local.example` - Template for local development
- `frontend/.env.docker.example` - Template for Docker deployment
- `frontend/src/lib/api.ts` - API utility functions

## Best Practices

1. **Never commit sensitive data**: Use `.env.example` for templates
2. **Separate configs**: Use `.env.local` for local dev, `.env` for Docker
3. **Use service names in Docker**: `backend`, not `localhost`
4. **Use localhost locally**: `localhost:8000`, not `backend:8000`
5. **Keep ports consistent**: Backend on 8000, Frontend on 3000
6. **Test both environments**: Verify local and Docker setups work

## Summary

The key difference between local and Docker setups:

| Environment | Frontend API URL | Backend Host | Backend Port |
|-------------|------------------|--------------|--------------|
| Local Dev   | `http://localhost:8000` | 0.0.0.0 | 8000 |
| Docker      | `http://backend:8000` | 0.0.0.0 | 8000 |

Both environments use the same backend port (8000) and frontend port (3000), but Docker uses service names for internal communication while local development uses localhost.
