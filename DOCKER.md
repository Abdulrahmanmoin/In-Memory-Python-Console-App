# Docker Deployment Guide

This guide provides instructions for building and deploying the Todo AI Chatbot application using Docker and Docker Compose.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Architecture Overview](#architecture-overview)
- [Building Images](#building-images)
- [Running with Docker Compose](#running-with-docker-compose)
- [Configuration](#configuration)
- [Health Checks](#health-checks)
- [Troubleshooting](#troubleshooting)
- [Production Considerations](#production-considerations)

## Prerequisites

- Docker Engine 20.10 or later
- Docker Compose v2.0 or later
- At least 4GB of available RAM
- Neon PostgreSQL database (or compatible PostgreSQL 14+)
- OpenAI API key (for AI features)

## Quick Start

1. Clone the repository and navigate to the project root:
   ```bash
   cd /path/to/todo_phase1
   ```

2. Copy the example environment file and configure it:
   ```bash
   cp .env.docker.example .env
   # Edit .env with your actual values
   ```

3. Build and start all services:
   ```bash
   docker-compose up --build -d
   ```

4. Verify services are running:
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Architecture Overview

### Multi-Stage Build Strategy

Both backend and frontend use multi-stage Docker builds to minimize image size and improve security:

**Backend (FastAPI)**
- Stage 1: Builder - Installs build dependencies and Python packages in virtual environment
- Stage 2: Production - Copies only runtime dependencies, runs as non-root user
- Base Image: `python:3.11.11-slim`
- Target Size: < 500MB

**Frontend (Next.js)**
- Stage 1: Dependencies - Installs npm packages
- Stage 2: Builder - Builds Next.js application with standalone output
- Stage 3: Production - Copies only built artifacts, runs as non-root user
- Base Image: `node:18.20.5-alpine`
- Target Size: < 500MB

### Service Communication

```
┌─────────────┐         ┌─────────────┐
│   Frontend  │         │   Backend   │
│  (Next.js)  │◄───────►│  (FastAPI)  │
│  Port 3000  │         │  Port 8000  │
└─────────────┘         └─────────────┘
       │                       │
       │                       │
       └───────┬───────────────┘
               │
               ▼
       ┌───────────────┐
       │ PostgreSQL DB │
       │ (Neon/Cloud)  │
       └───────────────┘
```

Services communicate over a dedicated Docker bridge network (`todo-network`).

## Building Images

### Build Individual Services

**Backend:**
```bash
cd backend
docker build -t todo-backend:v1.0.0 .
```

**Frontend:**
```bash
cd frontend
docker build -t todo-frontend:v1.0.0 .
```

### Build with Docker Compose

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build with no cache (clean build)
docker-compose build --no-cache
```

### Image Tagging Strategy

Images follow semantic versioning:
- `todo-backend:latest` - Latest stable build
- `todo-backend:v1.0.0` - Specific version
- `todo-backend:v1.0.0-sha-abc123` - Version with git SHA (CI/CD)

## Running with Docker Compose

### Start Services

```bash
# Start in foreground (logs visible)
docker-compose up

# Start in background (detached)
docker-compose up -d

# Start specific service
docker-compose up backend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (data loss!)
docker-compose down -v

# Stop specific service
docker-compose stop backend
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Restart Services

```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

## Configuration

### Environment Variables

Required environment variables are documented in `.env.docker.example`. Key configurations:

**Database:**
- `DATABASE_URL` - PostgreSQL connection string (required)

**Backend:**
- `SECRET_KEY` - Application secret key (generate with `openssl rand -hex 32`)
- `JWT_SECRET_KEY` - JWT signing key (generate with `openssl rand -hex 32`)
- `OPENAI_API_KEY` - OpenAI API key (required for AI features)
- `ALLOWED_ORIGINS` - CORS allowed origins (comma-separated)

**Frontend:**
- `NEXT_PUBLIC_API_URL` - Backend API URL for client-side requests
- `BACKEND_URL` - Backend API URL for server-side requests
- `BETTER_AUTH_SECRET` - Better Auth secret (generate with `openssl rand -base64 32`)
- `BETTER_AUTH_URL` - Frontend URL for authentication callbacks

### Generate Secret Keys

```bash
# Generate SECRET_KEY and JWT_SECRET_KEY
openssl rand -hex 32

# Generate BETTER_AUTH_SECRET
openssl rand -base64 32
```

### Runtime Configuration

Override environment variables at runtime:

```bash
# Pass environment variables
docker-compose up -d -e DATABASE_URL="postgresql+asyncpg://..."

# Use different env file
docker-compose --env-file .env.production up -d
```

## Health Checks

Both services include comprehensive health checks:

**Backend (`/health`):**
- Interval: 30s
- Timeout: 3s
- Start Period: 10s
- Retries: 3

**Frontend (`/api/health`):**
- Interval: 30s
- Timeout: 3s
- Start Period: 15s (Next.js may take longer to start)
- Retries: 3

### Check Health Status

```bash
# Docker Compose health status
docker-compose ps

# Detailed container inspection
docker inspect todo-backend | jq '.[0].State.Health'

# Manual health check
curl http://localhost:8000/health
curl http://localhost:3000/api/health
```

## Troubleshooting

### Container Won't Start

```bash
# Check container logs
docker-compose logs backend

# Check container status
docker-compose ps

# Inspect container details
docker inspect todo-backend
```

### Database Connection Issues

```bash
# Verify DATABASE_URL is correct
docker-compose exec backend env | grep DATABASE_URL

# Test database connectivity
docker-compose exec backend curl -f http://localhost:8000/health
```

### Port Conflicts

If ports 3000 or 8000 are already in use:

```bash
# Stop conflicting services
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9

# Or modify docker-compose.yml ports:
# ports:
#   - "3001:3000"  # Map host 3001 to container 3000
```

### Image Size Too Large

```bash
# Check image sizes
docker images | grep todo

# Analyze image layers
docker history todo-backend:v1.0.0

# Remove dangling images
docker image prune -f
```

### Permission Denied Errors

Both services run as non-root users. If you encounter permission issues:

```bash
# Check container user
docker-compose exec backend whoami  # Should show: appuser
docker-compose exec frontend whoami # Should show: nextjs

# Fix file permissions (if needed)
chown -R 1001:1001 ./backend
chown -R 1001:1001 ./frontend
```

## Production Considerations

### Security

1. **Never commit `.env` files** - Use secrets management (AWS Secrets Manager, HashiCorp Vault)
2. **Use non-root users** - Already configured in Dockerfiles
3. **Minimize attack surface** - Multi-stage builds remove build dependencies
4. **Scan images regularly** - Use `docker scan` or Trivy
5. **Keep base images updated** - Pin versions but update regularly

### Performance

1. **Resource Limits** - Configured in docker-compose.yml:
   - CPU: 1 core limit, 0.5 core reservation
   - Memory: 1GB limit, 512MB reservation

2. **Adjust for your workload:**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2.0'
         memory: 2G
   ```

3. **Scaling** - Use Docker Swarm or Kubernetes for horizontal scaling

### Logging

Logs are configured with rotation:
- Max size: 10MB per file
- Max files: 3 files
- Total log space: ~30MB per service

For production, consider:
- Centralized logging (ELK Stack, Splunk, Datadog)
- Structured JSON logging
- Log aggregation services

### Monitoring

Add monitoring tools:
- Prometheus + Grafana for metrics
- Sentry for error tracking
- New Relic or Datadog for APM

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
- name: Build and push Docker images
  run: |
    docker build -t myregistry/todo-backend:${{ github.sha }} ./backend
    docker push myregistry/todo-backend:${{ github.sha }}
```

### Kubernetes Deployment

These Dockerfiles are Kubernetes-ready:
- Non-root users
- Health checks via HTTP endpoints
- Environment variable configuration
- Graceful shutdown handling (dumb-init in frontend)

Next steps: Create Kubernetes manifests or Helm charts (see `specs/002-k8s-deployment/`)

## Additional Resources

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Next.js Docker Deployment](https://nextjs.org/docs/deployment#docker-image)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## Support

For issues or questions:
1. Check application logs: `docker-compose logs -f`
2. Review this documentation
3. Check GitHub issues
4. Contact the development team
