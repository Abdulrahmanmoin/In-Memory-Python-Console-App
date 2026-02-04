# Kubernetes Deployment Guide - Todo Chatbot

**Application**: Cloud Native Todo Chatbot
**Version**: 1.0.0
**Date**: 2026-01-27

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Deployment Guide](#detailed-deployment-guide)
4. [Verification](#verification)
5. [Troubleshooting](#troubleshooting)
6. [AI Tools Usage](#ai-tools-usage)
7. [Scaling and Updating](#scaling-and-updating)
8. [Cleanup](#cleanup)

---

## Prerequisites

### Required Tools

Ensure the following tools are installed:

| Tool | Version | Purpose | Installation |
|------|---------|---------|--------------|
| Docker Desktop | Latest | Container runtime | https://docs.docker.com/desktop/ |
| Minikube | v1.30+ | Local Kubernetes cluster | https://minikube.sigs.k8s.io/docs/start/ |
| kubectl | v1.28+ | Kubernetes CLI | https://kubernetes.io/docs/tasks/tools/ |
| Helm | v3.0+ | Kubernetes package manager | https://helm.sh/docs/intro/install/ |
| kubectl-ai | Latest | AI-assisted K8s operations (optional) | Check project docs |

### System Requirements

- **CPU**: 4 cores minimum (for Minikube)
- **RAM**: 8GB minimum (for Minikube)
- **Disk**: 10GB free space
- **OS**: Windows 10/11 with WSL 2, macOS, or Linux

### WSL 2 Setup (Windows Only)

1. Open Docker Desktop
2. Go to **Settings → Resources → WSL Integration**
3. Enable integration for your WSL distribution (e.g., Ubuntu-22.04)
4. Click **Apply & Restart**
5. Verify in WSL: `docker --version`

---

## Quick Start

**Estimated time**: 10-15 minutes

```bash
# 1. Setup Minikube
./scripts/setup-minikube.sh

# 2. Configure Docker environment
eval $(minikube docker-env)

# 3. Build images
./scripts/build-images.sh

# 4. Create secrets (replace with your actual values)
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-key \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=BETTER_AUTH_SECRET=your-auth-secret

kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=postgresql://user:pass@host/db

# 5. Deploy application
./scripts/deploy.sh dev

# 6. Access application
minikube service todo-chatbot-frontend --url
```

Open the URL in your browser to access the Todo Chatbot!

---

## Detailed Deployment Guide

### Step 1: Minikube Setup

Initialize a Minikube cluster with required resources:

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

**Expected output**: Node should show "Ready" status.

### Step 2: Configure Docker Environment

Point Docker CLI to Minikube's Docker daemon:

```bash
# Configure environment
eval $(minikube docker-env)

# Verify (should show Minikube containers)
docker ps
```

**Why**: This allows images built locally to be directly available in Minikube without pushing to a registry.

### Step 3: Build Container Images

Build both frontend and backend images:

```bash
# Build backend
cd backend
docker build -t todo-backend:v1.0.0 .
cd ..

# Build frontend
cd frontend
docker build -t todo-frontend:v1.0.0 .
cd ..

# Verify images
docker images | grep todo
minikube image ls | grep todo
```

**Expected sizes**:
- Backend: < 500MB
- Frontend: < 500MB

### Step 4: Create Kubernetes Secrets

Create secrets for sensitive data:

```bash
# Backend application secrets
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=sk-your-openai-key \
  --from-literal=SECRET_KEY=your-application-secret-key \
  --from-literal=BETTER_AUTH_SECRET=your-better-auth-secret

# Database connection secrets
kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=postgresql+psycopg://user:password@host:5432/dbname?sslmode=require

# Verify secrets were created
kubectl get secrets
```

**Security note**: Never commit secrets to version control. Use environment-specific secret management in production.

### Step 5: Deploy with Helm

Deploy the application using Helm charts:

```bash
# Development environment (1 replica, reduced resources)
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --values ./helm-charts/todo-chatbot/values-dev.yaml

# OR Production environment (3 replicas, full resources)
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --values ./helm-charts/todo-chatbot/values-prod.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=todo-chatbot --timeout=2m
```

### Step 6: Access the Application

Get the frontend URL and open in browser:

```bash
# Get URL
minikube service todo-chatbot-frontend --url

# OR open directly in browser
minikube service todo-chatbot-frontend
```

**Expected**: Frontend should load at `http://<minikube-ip>:30080`

---

## Verification

### Check Deployment Status

```bash
# View all resources
kubectl get all

# Check deployments
kubectl get deployments
# Expected: 2 deployments (backend, frontend), both READY

# Check pods
kubectl get pods
# Expected: 2+ backend pods, 2+ frontend pods, all Running

# Check services
kubectl get services
# Expected: backend (ClusterIP), frontend (NodePort)
```

### Test Health Endpoints

```bash
# Backend health check
kubectl port-forward svc/todo-chatbot-backend 8000:8000 &
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Frontend health check
FRONTEND_POD=$(kubectl get pod -l component=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl exec $FRONTEND_POD -- wget -qO- http://localhost:3000/api/health
# Expected: {"status":"healthy"}
```

### Test CRUD Operations

1. Open frontend URL in browser
2. Sign up / Log in
3. Create a new todo item
4. Update the todo item
5. Mark it as complete
6. Delete the todo item
7. Verify persistence by refreshing the page

---

## Troubleshooting

### Issue: Pods Not Starting

**Symptom**: Pods stuck in `Pending`, `CrashLoopBackOff`, or `ImagePullBackOff` state

```bash
# Check pod status
kubectl get pods

# View pod details
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>
```

**Solutions**:

1. **ImagePullBackOff**: Images not found
   ```bash
   # Verify Docker env is set
   eval $(minikube docker-env)

   # Rebuild images
   ./scripts/build-images.sh

   # Verify images in Minikube
   minikube image ls | grep todo
   ```

2. **CrashLoopBackOff**: Container crashes on startup
   ```bash
   # Check logs for errors
   kubectl logs <pod-name>

   # Common causes:
   # - Missing secrets: kubectl get secrets
   # - Database connection failure: Check DATABASE_URL
   # - Port conflicts: Check service configurations
   ```

3. **Pending**: Insufficient resources
   ```bash
   # Check node resources
   kubectl describe nodes

   # Reduce replicas temporarily
   kubectl scale deployment/todo-chatbot-backend --replicas=1
   kubectl scale deployment/todo-chatbot-frontend --replicas=1
   ```

### Issue: Secrets Missing

**Symptom**: Pods fail with environment variable errors

```bash
# Check if secrets exist
kubectl get secrets

# If missing, create them
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=SECRET_KEY=... \
  --from-literal=BETTER_AUTH_SECRET=...

kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=postgresql://...

# Restart pods to pick up secrets
kubectl rollout restart deployment/todo-chatbot-backend
kubectl rollout restart deployment/todo-chatbot-frontend
```

### Issue: Minikube Out of Resources

**Symptom**: Pods pending due to insufficient CPU/memory

```bash
# Check resource usage
kubectl top nodes
kubectl top pods

# Options:
# 1. Reduce replicas in values file
# 2. Use values-dev.yaml (lower resource limits)
# 3. Restart Minikube with more resources
minikube stop
minikube start --cpus=6 --memory=10240
```

### Issue: Cannot Access Frontend

**Symptom**: Frontend URL not reachable

```bash
# Check service
kubectl get svc todo-chatbot-frontend

# Verify NodePort service
minikube service list

# Get URL
minikube service todo-chatbot-frontend --url

# Check if pods are ready
kubectl get pods -l component=frontend

# Check logs
kubectl logs -l component=frontend
```

### Issue: Frontend Cannot Connect to Backend

**Symptom**: API calls fail in browser console

```bash
# Check backend service
kubectl get svc todo-chatbot-backend

# Verify DNS resolution from frontend pod
FRONTEND_POD=$(kubectl get pod -l component=frontend -o jsonpath='{.items[0].metadata.name}')
kubectl exec $FRONTEND_POD -- nslookup todo-chatbot-backend

# Test backend connectivity
kubectl exec $FRONTEND_POD -- wget -qO- http://todo-chatbot-backend:8000/health

# Check ConfigMap for BACKEND_URL
kubectl get configmap todo-chatbot-config -o yaml
```

---

## AI Tools Usage

### kubectl-ai Commands

kubectl-ai simplifies Kubernetes operations with natural language:

```bash
# Check deployment status
kubectl-ai "show me the status of all deployments"

# Troubleshoot pod issues
kubectl-ai "check why the pods are failing"

# Scale deployments
kubectl-ai "scale the frontend deployment to 3 replicas"

# View logs
kubectl-ai "show me the logs of the backend pod"

# Describe resources
kubectl-ai "describe the frontend service"

# Check resource usage
kubectl-ai "show me which pods are using the most memory"
```

All AI tool usage is documented in `AI-TOOLS-LOG.md`.

### Gordon (Docker AI) Commands

If Gordon is available:

```bash
# Analyze Dockerfile security
docker ai "Analyze my Dockerfile for security best practices"

# Optimize image size
docker ai "How can I reduce the size of this Docker image?"

# Troubleshoot build issues
docker ai "Why is my Docker build failing?"
```

**Note**: Gordon was not available in this environment. Standard Docker CLI and manual reviews were used as fallbacks.

---

## Scaling and Updating

### Scale Deployments

```bash
# Manual scaling
kubectl scale deployment/todo-chatbot-backend --replicas=5
kubectl scale deployment/todo-chatbot-frontend --replicas=3

# Using Helm upgrade
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=3

# Verify scaling
kubectl get deployments
```

### Update Configuration

```bash
# Edit ConfigMap
kubectl edit configmap todo-chatbot-config

# Restart pods to pick up changes
kubectl rollout restart deployment/todo-chatbot-backend
kubectl rollout restart deployment/todo-chatbot-frontend

# OR use Helm upgrade
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --values ./helm-charts/todo-chatbot/values-prod.yaml
```

### Update Container Images

```bash
# Build new images with new tag
docker build -t todo-backend:v1.1.0 ./backend
docker build -t todo-frontend:v1.1.0 ./frontend

# Update Helm values
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.image.tag=v1.1.0 \
  --set frontend.image.tag=v1.1.0

# Verify rollout
kubectl rollout status deployment/todo-chatbot-backend
kubectl rollout status deployment/todo-chatbot-frontend
```

### Rollback Deployment

```bash
# View deployment history
helm history todo-chatbot

# Rollback to previous revision
helm rollback todo-chatbot

# Rollback to specific revision
helm rollback todo-chatbot 2

# Verify rollback
kubectl get pods
helm list
```

---

## Cleanup

### Remove Application Only

```bash
# Uninstall Helm release
helm uninstall todo-chatbot

# Verify removal
kubectl get all
```

### Full Cleanup (Application + Secrets)

```bash
# Uninstall application
helm uninstall todo-chatbot

# Delete secrets
kubectl delete secret todo-backend-secrets
kubectl delete secret todo-database-secrets

# Verify namespace is clean
kubectl get all
```

### Stop Minikube

```bash
# Stop cluster (preserves state)
minikube stop

# Delete cluster completely
minikube delete
```

### Use Teardown Script

```bash
# Interactive teardown script
./scripts/teardown.sh

# Script will prompt for:
# - Uninstall Helm release
# - Stop Minikube
# - Delete Minikube cluster
```

---

## Additional Resources

### Helm Commands Reference

```bash
# List releases
helm list

# Get release status
helm status todo-chatbot

# View chart values
helm get values todo-chatbot

# Render templates locally (dry-run)
helm template todo-chatbot ./helm-charts/todo-chatbot

# Validate chart
helm lint ./helm-charts/todo-chatbot
```

### Kubectl Commands Reference

```bash
# Get resources
kubectl get <resource>  # pods, deployments, services, configmaps, secrets

# Describe resource
kubectl describe <resource> <name>

# View logs
kubectl logs <pod-name>
kubectl logs -f <pod-name>  # Follow logs
kubectl logs -l app=todo-chatbot  # All pods with label

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/sh

# Port forwarding
kubectl port-forward <pod-name> 8000:8000

# Get pod YAML
kubectl get pod <pod-name> -o yaml
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      Minikube Cluster                   │
│                                                         │
│  ┌──────────────┐              ┌──────────────┐       │
│  │   Frontend   │              │   Backend    │       │
│  │   (Next.js)  │              │  (FastAPI)   │       │
│  │              │─────────────▶│              │       │
│  │  Port: 3000  │  Internal    │  Port: 8000  │       │
│  │  Replicas: 2 │  ClusterIP   │  Replicas: 2 │       │
│  └──────┬───────┘              └──────┬───────┘       │
│         │                              │               │
│         │                              │               │
│  ┌──────▼───────┐              ┌──────▼───────┐       │
│  │   Frontend   │              │   Backend    │       │
│  │   Service    │              │   Service    │       │
│  │  (NodePort)  │              │ (ClusterIP)  │       │
│  │  Port: 30080 │              │  Port: 8000  │       │
│  └──────────────┘              └──────────────┘       │
│                                                         │
│  ┌─────────────────────────────────────────────┐      │
│  │           ConfigMap & Secrets               │      │
│  │  - BACKEND_URL, NODE_ENV, LOG_LEVEL        │      │
│  │  - OPENAI_API_KEY, SECRET_KEY, DB_URL      │      │
│  └─────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
                      │
                      │ External Access
                      ▼
            http://<minikube-ip>:30080
                  (Browser)
                      │
                      │ Database Connection
                      ▼
         ┌────────────────────────┐
         │  Neon PostgreSQL       │
         │  (External Service)    │
         └────────────────────────┘
```

---

## Support

- **Documentation**: See `helm-charts/todo-chatbot/README.md` for Helm chart details
- **Configuration**: See `helm-charts/todo-chatbot/CONFIGURATION.md` for all options
- **AI Tools Log**: See `AI-TOOLS-LOG.md` for AI-assisted operations tracking
- **Issues**: Check troubleshooting section or create an issue in the repository

---

**Last Updated**: 2026-01-27
**Version**: 1.0.0
