# Testing Guide - Frontend-Backend Integration

## Quick Start Testing

### 1. Local Development Testing

#### Start Backend
```bash
cd backend
python -m src.main
# Backend should start on http://localhost:8000
```

Expected output:
```
Application starting up...
Database initialized successfully.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

#### Start Frontend
```bash
cd frontend
npm run dev
# Frontend should start on http://localhost:3000
```

Expected output:
```
▲ Next.js 14.x.x
- Local:        http://localhost:3000
```

#### Test Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

#### Test API Documentation
Open in browser: `http://localhost:8000/docs`
- Should see Swagger UI with all API endpoints

### 2. Docker Testing

#### Build and Start
```bash
docker-compose up --build
```

Expected output:
```
✔ Container todo-backend started
✔ Container todo-frontend started
```

#### Test Backend Health (Docker)
```bash
curl http://localhost:8000/health
```

or

```bash
docker exec todo-backend curl -f http://localhost:8000/health
```

#### Test Frontend Access
Open in browser: `http://localhost:3000`

#### Test Inter-Service Communication
```bash
docker exec todo-frontend curl -f http://backend:8000/health
```

Expected: Should return `{"status":"healthy"}`

### 3. API Endpoint Testing

#### Register User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123"
  }'
```

Expected: Returns user data and JWT token

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

Expected: Returns JWT token
```json
{
  "token": "eyJ...",
  "user": {...}
}
```

#### Create Task (Authenticated)
```bash
# First, get the token from login response
TOKEN="your_jwt_token_here"
USER_ID="your_user_id_here"

curl -X POST http://localhost:8000/api/${USER_ID}/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{
    "title": "Test Task",
    "description": "This is a test task"
  }'
```

Expected: Returns created task
```json
{
  "task_id": "uuid",
  "title": "Test Task",
  "description": "This is a test task",
  "is_completed": false,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Get All Tasks
```bash
curl -X GET http://localhost:8000/api/${USER_ID}/tasks \
  -H "Authorization: Bearer ${TOKEN}"
```

Expected: Returns array of tasks

### 4. Frontend UI Testing

#### Manual Test Checklist

1. **Registration Flow**
   - [ ] Navigate to `http://localhost:3000/register`
   - [ ] Fill in email, username, password
   - [ ] Click "Register"
   - [ ] Should redirect to tasks page or login

2. **Login Flow**
   - [ ] Navigate to `http://localhost:3000/login`
   - [ ] Enter credentials
   - [ ] Click "Login"
   - [ ] Should redirect to tasks page

3. **Task Creation**
   - [ ] Click "Add New Task" button
   - [ ] Enter task title and description
   - [ ] Click "Create Task"
   - [ ] New task should appear in list

4. **Task Completion**
   - [ ] Click checkbox next to a task
   - [ ] Task should show as completed (strikethrough)
   - [ ] Click again to mark as incomplete

5. **Task Update**
   - [ ] Click "Edit" button on a task
   - [ ] Modify title or description
   - [ ] Click "Update Task"
   - [ ] Changes should be saved

6. **Task Deletion**
   - [ ] Click "Delete" button on a task
   - [ ] Task should be removed from list

### 5. Network Inspection

#### Browser DevTools
1. Open browser DevTools (F12)
2. Go to Network tab
3. Perform actions (login, create task, etc.)
4. Verify:
   - [ ] Requests go to correct URL (http://localhost:8000 or http://backend:8000)
   - [ ] Status codes are 200/201 for success
   - [ ] Authorization header is present
   - [ ] No CORS errors

#### Expected Request Headers
```
Authorization: Bearer eyJ...
Content-Type: application/json
```

#### Expected Response Headers
```
Access-Control-Allow-Origin: http://localhost:3000
Content-Type: application/json
```

### 6. Docker Health Checks

#### Check Container Health
```bash
docker ps
```

Look for "healthy" status:
```
CONTAINER ID   IMAGE              STATUS
abc123         todo-backend:v1    Up 2 minutes (healthy)
def456         todo-frontend:v1   Up 2 minutes (healthy)
```

#### View Container Logs
```bash
# Backend logs
docker logs todo-backend

# Frontend logs
docker logs todo-frontend

# Follow logs in real-time
docker logs -f todo-backend
```

### 7. Common Issues and Debugging

#### Issue: Connection Refused

**Check if services are running:**
```bash
# Local
netstat -an | grep 8000
netstat -an | grep 3000

# Docker
docker ps
docker-compose ps
```

**Solution**: Start the respective service

#### Issue: CORS Error

**Check backend logs for CORS configuration:**
```bash
docker logs todo-backend | grep CORS
```

**Solution**: Verify ALLOWED_ORIGINS includes frontend URL

#### Issue: 401 Unauthorized

**Check token:**
```bash
# In browser console
console.log(localStorage.getItem('authToken'))
```

**Solution**: Re-login to get fresh token

#### Issue: Database Connection Error

**Check DATABASE_URL:**
```bash
# Local
cd backend && python3 -c "from src.config import settings; print(settings.DATABASE_URL)"

# Docker
docker exec todo-backend printenv DATABASE_URL
```

**Solution**: Verify database credentials and network connectivity

### 8. Performance Testing

#### Response Time Test
```bash
# Test backend health endpoint
time curl http://localhost:8000/health

# Should be < 100ms
```

#### Load Test (Optional)
```bash
# Install hey (HTTP load tester)
# brew install hey (macOS) or apt install hey (Linux)

# Test with 100 requests, 10 concurrent
hey -n 100 -c 10 http://localhost:8000/health
```

### 9. Integration Test Script

Create `test-integration.sh`:
```bash
#!/bin/bash

echo "Testing Backend Health..."
curl -f http://localhost:8000/health || { echo "Backend health check failed"; exit 1; }

echo "Testing Frontend..."
curl -f http://localhost:3000 > /dev/null || { echo "Frontend not accessible"; exit 1; }

echo "Testing API Documentation..."
curl -f http://localhost:8000/docs > /dev/null || { echo "API docs not accessible"; exit 1; }

echo "All tests passed!"
```

Run:
```bash
chmod +x test-integration.sh
./test-integration.sh
```

## Success Criteria

✅ Backend health endpoint returns `{"status":"healthy"}`
✅ Frontend loads without errors
✅ User can register successfully
✅ User can login successfully
✅ User can create tasks
✅ User can update tasks
✅ User can delete tasks
✅ User can toggle task completion
✅ No CORS errors in browser console
✅ All API calls show 2xx status codes
✅ Docker containers are healthy

## Troubleshooting Resources

- **Backend Logs**: Check for Python exceptions and database errors
- **Frontend Logs**: Check browser console for network errors
- **Docker Logs**: Check container logs for startup errors
- **API Docs**: Use Swagger UI at `/docs` to test endpoints directly
- **Setup Guide**: See FRONTEND-BACKEND-SETUP.md for configuration details
