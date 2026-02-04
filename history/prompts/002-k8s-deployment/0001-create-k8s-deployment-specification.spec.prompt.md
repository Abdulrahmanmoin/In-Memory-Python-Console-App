---
id: 0001
title: Create K8s deployment specification
stage: spec
date: 2026-01-25
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-k8s-deployment
branch: 002-k8s-deployment
user: Claude
command: /sp.specify
labels: ["kubernetes", "deployment", "containerization", "helm", "minikube", "specification"]
links:
  spec: specs/002-k8s-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-k8s-deployment/spec.md
  - specs/002-k8s-deployment/checklists/requirements.md
tests:
  - none
---

## Prompt

# Project Specification: Cloud Native Todo Chatbot - Local Kubernetes Deployment

## Project Overview
Deploy the existing Todo Chatbot application (completed in Phase III) onto a local Kubernetes cluster using containerization and orchestration best practices with AI-assisted DevOps tooling.

## Phase Context
- **Current Phase:** Phase IV - Local Kubernetes Deployment
- **Deployment Target:** Local Minikube cluster

## Requirements Specification

### 1. Containerization Requirements
#### 1.1 Frontend Container
- Create a production-ready Dockerfile for the frontend application
- Use multi-stage builds to minimize image size
- Expose appropriate port (typically 3000)
- Include health check configuration
- Use Gordon (Docker AI Agent) for AI-assisted Docker operations where available
- Fallback: Use standard Docker CLI or Claude Code generated commands if Gordon unavailable

#### 1.2 Backend Container
- Create a production-ready Dockerfile for the backend application
- Configure environment variables for database/service connections
- Include health check and readiness probe support
- Optimize for container best practices (non-root user, minimal base image)

#### 1.3 Docker Compose (Local Testing)
- Create docker-compose.yml for local multi-container testing before K8s deployment
- Define service dependencies and networking
- Include volume mounts for development if needed

### 2. Helm Chart Requirements
#### 2.1 Chart Structure
Generate Helm charts with standard structure including Chart.yaml, values.yaml, templates for deployments, services, configmaps, secrets, and optional ingress/HPA.

#### 2.2 Frontend & Backend Helm Templates
- Deployment with configurable replicas (default: 2)
- Service configuration (ClusterIP/NodePort)
- Resource limits and requests defined
- Liveness and readiness probes configured
- Environment variables from ConfigMap
- Secrets management for sensitive data

#### 2.4 Values Configuration
- Parameterize image tags, replica counts, resource limits
- Environment-specific overrides (dev, staging, prod)
- Enable/disable optional components (ingress, HPA)

### 3. Kubernetes Deployment Requirements
#### 3.1 Minikube Setup
- Document Minikube start command with appropriate resources
- Enable required addons (ingress, metrics-server if needed)
- Configure Docker environment for Minikube

#### 3.2 Deployment Process
- Build and tag Docker images locally
- Load images into Minikube
- Deploy using Helm install/upgrade commands
- Verify deployment with kubectl commands

#### 3.3 Networking
- Frontend accessible via NodePort or Minikube tunnel
- Backend accessible internally within cluster
- Service discovery between frontend and backend

### 4. AI-Assisted DevOps Integration
- Use kubectl-ai for Kubernetes operations
- Optional Gordon usage for Docker operations
- Document all AI tool interactions

## Acceptance Criteria
### Must Have (P0)
- Frontend and Backend Dockerfiles created and build successfully
- Containers run locally via Docker
- Helm chart structure created with all required templates
- Minikube cluster running with sufficient resources
- Frontend and backend deployments running with 2+ replicas each
- Frontend accessible via browser, backend API functional
- Todo CRUD operations work end-to-end in K8s environment

### Should Have (P1)
- Health checks configured
- Resource limits and requests defined
- ConfigMaps for environment configuration
- kubectl-ai used for at least 3 operations
- Deployment documented with clear instructions

### Nice to Have (P2)
- Gordon used for Docker operations
- Horizontal Pod Autoscaler configured
- Ingress configured
- Secrets properly managed

## Constraints & Considerations
### Technical Constraints
- Must use Minikube (not cloud K8s)
- Must use Helm for deployment (not raw manifests)
- Should leverage AI tools where possible
- Images must be loadable into Minikube

### Resource Constraints
- Minikube recommended: 4 CPU, 8GB RAM minimum
- Keep container images small (<500MB each ideally)

## Deliverables
1. Dockerfiles for frontend and backend
2. docker-compose.yml for local testing
3. Complete Helm chart directory
4. Deployment scripts (setup-minikube.sh, build-images.sh, deploy.sh, teardown.sh)
5. K8S-DEPLOYMENT.md documentation
6. AI tools usage log

## Response snapshot

Created comprehensive specification for Cloud Native Todo Chatbot - Local Kubernetes Deployment feature on branch 002-k8s-deployment. Specification includes 5 prioritized user stories (P0-P2), 29 functional requirements organized by category (Containerization, Helm Charts, Kubernetes Deployment, Resource Management, AI-Assisted Operations, Documentation), 16 success criteria with measurable outcomes, and detailed assumptions, constraints, dependencies, and scope boundaries.

Resolved 3 critical clarifications through user interaction:
1. Database connectivity: Keep Neon PostgreSQL external to cluster
2. Better Auth secrets: Kubernetes Secret created manually before deployment
3. Frontend-Backend communication: Environment variable injected via ConfigMap

Created specification quality checklist with all validation items passing. Feature is ready for implementation planning with `/sp.plan`.

## Outcome

- ✅ Impact: Created production-ready specification for Phase IV Kubernetes deployment; established clear requirements for containerization, Helm charts, and AI-assisted DevOps workflows
- 🧪 Tests: No tests required (specification phase)
- 📁 Files: Created specs/002-k8s-deployment/spec.md (275 lines) and specs/002-k8s-deployment/checklists/requirements.md
- 🔁 Next prompts: Run `/sp.plan` to create implementation architecture, or `/sp.clarify` for additional requirement refinement if needed
- 🧠 Reflection: Specification follows SDD methodology with clear separation of WHAT (user needs) from HOW (implementation); all 3 clarifications resolved efficiently through structured Q&A format

## Evaluation notes (flywheel)

- Failure modes observed: None; specification creation followed template structure and validation process successfully
- Graders run and results (PASS/FAIL): Specification Quality Checklist - PASSED (all items checked)
- Prompt variant (if applicable): Standard /sp.specify workflow with clarification resolution
- Next experiment (smallest change to try): Proceed to planning phase to validate architectural approach for Kubernetes deployment
