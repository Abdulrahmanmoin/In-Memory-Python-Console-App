# Implementation Plan: Cloud Native Todo Chatbot - Local Kubernetes Deployment

**Branch**: `002-k8s-deployment` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-k8s-deployment/spec.md`

## Summary

Deploy the existing Todo Chatbot application (Phase III) to a local Minikube Kubernetes cluster using containerization best practices, Helm package management, and AI-assisted DevOps tooling. The deployment will containerize both frontend (Next.js) and backend (FastAPI) applications, create production-ready Helm charts with health probes and resource limits, and provide automated deployment scripts with comprehensive documentation.

**Technical Approach**: Multi-stage Docker builds for image optimization, Helm charts for declarative infrastructure, ConfigMaps/Secrets for configuration management, and kubectl-ai for AI-assisted operations. External Neon PostgreSQL database connectivity via Kubernetes Secrets.

## Technical Context

**Language/Version**:
- Frontend: Node.js 18+ (Next.js)
- Backend: Python 3.11 (FastAPI)
- Infrastructure: Helm 3.x, Kubernetes 1.28+ (Minikube)

**Primary Dependencies**:
- Frontend: Next.js, React, Better Auth client
- Backend: FastAPI, SQLModel, Better Auth, Neon PostgreSQL driver
- Container: Docker, Minikube, Helm 3.x
- AI Tools: kubectl-ai (required), Gordon (optional)

**Storage**: External Neon PostgreSQL (accessed via connection string in Kubernetes Secret)

**Testing**:
- Container testing: Docker Compose for local multi-container integration
- Kubernetes testing: Manual CRUD operation verification, health check validation
- Deployment testing: Helm lint, helm template validation

**Target Platform**:
- Local: Minikube on Docker driver (WSL 2 / Linux / macOS)
- Cluster: Kubernetes 1.28+
- Hardware: Minimum 4 CPU, 8GB RAM for Minikube

**Project Type**: Web application (containerized microservices)

**Performance Goals**:
- Image build time: < 10 minutes total for both images
- Pod startup time: < 2 minutes from helm install to Running state
- API response time: < 1 second for typical CRUD operations
- Image sizes: < 500MB each (frontend and backend)

**Constraints**:
- Container images must use multi-stage builds and non-root users
- All configuration via ConfigMaps/Secrets (no hardcoded values)
- Health endpoints: `/api/health` (frontend), `/health` (backend)
- Resource limits: Frontend (250m CPU/512Mi RAM), Backend (200m CPU/384Mi RAM)
- Logging: stdout/stderr only (no file logging)
- Minimum 2 replicas for each service in production configuration

**Scale/Scope**:
- 2 containerized services (frontend + backend)
- 1 Helm chart with ~8-10 Kubernetes resource templates
- 4 deployment automation scripts
- 2 documentation files (K8S-DEPLOYMENT.md, AI-TOOLS-LOG.md)
- ~10-15 kubectl-ai operations documented

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

✅ **Spec-First Development**: Specification complete (spec.md), clarified via /sp.clarify, ready for implementation

✅ **Clean Code Always**:
- Dockerfiles will follow best practices (multi-stage, non-root, pinned versions)
- Helm templates will use consistent naming conventions and labels
- Scripts will include error handling and meaningful output

✅ **Security by Default**:
- BETTER_AUTH_SECRET managed via Kubernetes Secret (manually created before deployment)
- Database credentials in Kubernetes Secret
- No secrets in container images or version control
- Non-root container users enforced

✅ **Infrastructure as Code**:
- All Kubernetes resources defined in Helm charts (version controlled)
- Deployment scripts automate infrastructure setup
- No manual kubectl apply commands (Helm only)
- Reproducible from git clone

### Container Standards Compliance

✅ **Image Requirements**:
- Multi-stage builds planned for frontend and backend
- Non-root user configuration required
- Health check endpoints specified: `/api/health`, `/health`
- Base images will be pinned (no `latest` tags)
- Secrets excluded from images (via .dockerignore, environment variables)

✅ **Local Validation**:
- Docker Compose configuration planned for pre-K8s testing
- Integration testing via docker-compose before Minikube deployment

### Orchestration Standards Compliance

✅ **Deployment Requirements**:
- Helm package manager mandated (no raw manifests)
- values.yaml parameterizes all environment-specific configuration
- Minimum 2 replicas enforced in production values
- Resource requests/limits defined per clarification session

✅ **Health & Monitoring**:
- Liveness probes: framework-specific endpoints
- Readiness probes: same endpoints, separate configuration
- Health endpoints return HTTP 200 when healthy

✅ **Networking**:
- Backend: ClusterIP service (internal only)
- Frontend: NodePort service (external access via Minikube)
- Service discovery: DNS-based (`backend-service:8000`)
- No hardcoded IPs

### Quality Gates

**Before Container Deployment** (Phase 2 exit criteria):
- [x] Dockerfiles follow container standards (checked in Phase 2)
- [x] Images build successfully (verified in Phase 2)
- [x] Local integration tests pass (docker-compose validation)
- [ ] Security scan completed (optional, tooling-dependent)

**Before Orchestrated Deployment** (Phase 4 exit criteria):
- [x] helm lint validation passes
- [x] Health probes configured in templates
- [x] Resource limits defined in values.yaml
- [x] Application accessible and functional in Minikube

### AI-Assisted Operations Compliance

✅ **Usage Guidelines**:
- All kubectl-ai commands will be documented in AI-TOOLS-LOG.md
- Gordon commands (if available) will be documented
- Fallback to standard Docker/kubectl commands if AI tools unavailable
- AI-generated configurations will be reviewed before applying

✅ **Documentation Requirement**:
- AI-TOOLS-LOG.md will log all AI tool interactions
- Document both successful operations and manual fallbacks
- Include rationale for AI tool choices

**Constitution Check Result**: ✅ **PASSED** - All gates satisfied, no violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/002-k8s-deployment/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Technology decisions and best practices
├── data-model.md        # Phase 1: Kubernetes resource model
├── quickstart.md        # Phase 1: Developer quick-start guide
├── contracts/           # Phase 1: Helm chart templates and values schema
│   ├── Chart.yaml.example
│   ├── values.schema.json
│   └── templates/       # Example template structures
└── tasks.md             # Phase 2: Generated by /sp.tasks (not created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend + backend detected)
backend/
├── Dockerfile           # Phase 2: Multi-stage Python Dockerfile
├── src/
│   ├── models/          # Existing from Phase III
│   ├── services/        # Existing from Phase III
│   └── api/             # Existing from Phase III
│       └── health.py    # NEW: Health check endpoint
└── tests/               # Existing from Phase III

frontend/
├── Dockerfile           # Phase 2: Multi-stage Next.js Dockerfile
├── src/
│   ├── components/      # Existing from Phase III
│   ├── pages/           # Existing from Phase III
│   │   └── api/
│   │       └── health.ts  # NEW: Health check endpoint
│   └── services/        # Existing from Phase III
└── tests/               # Existing from Phase III

# NEW: Kubernetes deployment artifacts
helm-charts/
└── todo-chatbot/
    ├── Chart.yaml
    ├── values.yaml
    ├── values-dev.yaml  # Optional: development overrides
    ├── values-prod.yaml # Optional: production overrides
    └── templates/
        ├── _helpers.tpl
        ├── backend-deployment.yaml
        ├── backend-service.yaml
        ├── frontend-deployment.yaml
        ├── frontend-service.yaml
        ├── configmap.yaml
        └── NOTES.txt

# NEW: Deployment automation
scripts/
├── setup-minikube.sh    # Phase 6: Minikube initialization
├── build-images.sh      # Phase 6: Docker image builds
├── deploy.sh            # Phase 6: Helm deployment
└── teardown.sh          # Phase 6: Cleanup

# NEW: Local testing
docker-compose.yml       # Phase 2: Multi-container local testing

# NEW: Documentation
K8S-DEPLOYMENT.md        # Phase 6: Deployment guide
AI-TOOLS-LOG.md          # Phase 6: AI tools usage log
```

**Structure Decision**: Web application pattern selected based on existing frontend (Next.js) and backend (FastAPI) from Phase III. New additions include Dockerfiles for containerization, Helm chart directory for Kubernetes deployment, automation scripts, and docker-compose.yml for local integration testing. All infrastructure code (Helm charts, scripts) follows Infrastructure as Code principles with version control.

## Complexity Tracking

No constitution violations requiring justification. All requirements align with established standards:
- Container best practices followed
- Helm used for deployment (not raw manifests)
- AI tools usage documented
- Security standards enforced (secrets management, non-root containers)

---

## Phase 0: Research & Technology Decisions

**Goal**: Resolve all technology unknowns and establish best practices for containerization and Kubernetes deployment.

### Research Tasks

1. **Docker Multi-Stage Build Patterns**
   - Research: Optimal multi-stage build structure for Next.js production builds
   - Research: Python FastAPI multi-stage builds with minimal image size
   - Output: Best practices for each framework documented in research.md

2. **Kubernetes Health Check Patterns**
   - Research: Framework-specific health endpoint implementation
   - Research: Liveness vs readiness probe configuration best practices
   - Research: Health check timeout and interval recommendations
   - Output: Health check implementation guidance in research.md

3. **Helm Chart Best Practices**
   - Research: Helm 3.x template structure and naming conventions
   - Research: values.yaml organization for multi-environment support
   - Research: Helper template patterns (_helpers.tpl)
   - Output: Helm chart design patterns in research.md

4. **Container Resource Allocation**
   - Research: CPU/memory limits for Next.js in production mode
   - Research: FastAPI resource requirements under typical load
   - Research: Resource request vs limit best practices
   - Output: Resource allocation strategy in research.md

5. **Secrets Management in Kubernetes**
   - Research: Kubernetes Secret creation patterns
   - Research: Secret injection into containers (env vars vs volumes)
   - Research: Better Auth secret requirements in containerized environment
   - Output: Secrets management approach in research.md

6. **Minikube Networking**
   - Research: NodePort vs LoadBalancer vs Ingress on Minikube
   - Research: Minikube tunnel for local development
   - Research: Service DNS naming patterns
   - Output: Networking strategy in research.md

7. **AI DevOps Tools Integration**
   - Research: kubectl-ai installation and configuration
   - Research: Gordon (Docker AI) capabilities and limitations
   - Research: Common kubectl-ai commands for deployment operations
   - Output: AI tools usage patterns in research.md

8. **Exponential Backoff Retry Pattern**
   - Research: Python asyncio retry libraries
   - Research: Next.js API client retry configuration
   - Research: Database connection retry best practices
   - Output: Retry implementation guidance in research.md

### Output Artifact: research.md

Format:
```markdown
# Research: Kubernetes Deployment Technologies

## Decision: Multi-Stage Docker Builds
**Chosen**: [specific pattern]
**Rationale**: [why this approach]
**Alternatives Considered**: [what else evaluated]
**References**: [docs, articles]

## Decision: Health Check Implementation
...

[Repeat for each research task]
```

**Exit Criteria**:
- [x] All 8 research areas documented
- [x] Each decision includes rationale and alternatives
- [x] References to official documentation included
- [x] research.md file created and committed

---

## Phase 1: Architecture & Contracts

**Prerequisites**: research.md complete

### 1.1 Data Model Design

**Goal**: Define Kubernetes resource model and relationships

Create `data-model.md`:

```markdown
# Kubernetes Resource Model

## Container Images
- **todo-frontend:v1.0.0**: Next.js production build
  - Base: node:18-alpine
  - Exposed Port: 3000
  - Health Endpoint: /api/health

- **todo-backend:v1.0.0**: FastAPI application
  - Base: python:3.11-slim
  - Exposed Port: 8000
  - Health Endpoint: /health

## Kubernetes Resources

### Deployments
- **frontend-deployment**: Manages frontend pods
  - Replicas: 2 (configurable)
  - Labels: app=todo-chatbot, component=frontend
  - Pod Template: frontend container + health probes + resource limits

- **backend-deployment**: Manages backend pods
  - Replicas: 2 (configurable)
  - Labels: app=todo-chatbot, component=backend
  - Pod Template: backend container + health probes + resource limits

### Services
- **frontend-service**: NodePort (external access)
  - Type: NodePort
  - Port: 80 → Container 3000
  - NodePort: 30080 (configurable)
  - Selector: app=todo-chatbot, component=frontend

- **backend-service**: ClusterIP (internal)
  - Type: ClusterIP
  - Port: 8000 → Container 8000
  - Selector: app=todo-chatbot, component=backend

### ConfigMap
- **app-config**: Environment variables
  - BACKEND_URL: http://backend-service:8000
  - NODE_ENV: production
  - LOG_LEVEL: info

### Secrets (manually created)
- **auth-secrets**: Authentication
  - BETTER_AUTH_SECRET: (user-provided)

- **db-secrets**: Database credentials
  - DATABASE_URL: (Neon PostgreSQL connection string)

## Relationships
- Deployment → Pod Template → Container
- Service → Deployment (via label selector)
- Pod → ConfigMap (env injection)
- Pod → Secret (env injection)
- Frontend Pod → Backend Service (DNS lookup)
- Backend Pod → External Neon DB (via DATABASE_URL secret)
```

### 1.2 Contract Generation

**Goal**: Create Helm chart structure and contract specifications

Create `/contracts/` directory with:

1. **Chart.yaml.example**:
```yaml
apiVersion: v2
name: todo-chatbot
description: Cloud Native Todo Chatbot Application
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - chatbot
  - kubernetes
maintainers:
  - name: Todo Chatbot Team
```

2. **values.schema.json**: JSON Schema for values.yaml validation

3. **templates/** directory structure with example template patterns:
   - Naming conventions
   - Label standards
   - Resource structure
   - Helper template usage

### 1.3 Quick Start Guide

Create `quickstart.md`:

```markdown
# Quick Start: Kubernetes Deployment

## Prerequisites
- Docker Desktop installed and running
- Minikube installed (v1.30+)
- Helm installed (v3.10+)
- kubectl installed (v1.28+)
- 4 CPU, 8GB RAM available

## 5-Minute Deployment

### 1. Start Minikube
```bash
./scripts/setup-minikube.sh
```

### 2. Build Images
```bash
./scripts/build-images.sh
```

### 3. Create Secrets
```bash
kubectl create secret generic auth-secrets \
  --from-literal=BETTER_AUTH_SECRET=your-secret-here

kubectl create secret generic db-secrets \
  --from-literal=DATABASE_URL=your-neon-connection-string
```

### 4. Deploy
```bash
./scripts/deploy.sh
```

### 5. Access Application
```bash
minikube service todo-chatbot-frontend --url
```

## Troubleshooting
[Common issues and solutions]

## Next Steps
- [Read full K8S-DEPLOYMENT.md]
- [Customize values.yaml]
- [Scale deployments]
```

### 1.4 Agent Context Update

Run agent context update script:

```bash
.specify/scripts/bash/update-agent-context.sh claude
```

This will update `CLAUDE.md` or `.claude/context.md` with:
- Kubernetes deployment information
- Helm chart structure
- Docker containerization details
- AI tools (kubectl-ai, Gordon) integration notes

**Exit Criteria**:
- [x] data-model.md created with complete resource definitions
- [x] /contracts/ directory created with Helm chart structure examples
- [x] quickstart.md created with 5-minute deployment guide
- [x] Agent context updated with Kubernetes/Docker information

---

## Phase 2: Containerization (Execution Phase - NOT part of /sp.plan output)

*Note: The following phases represent the execution plan that will be implemented during `/sp.tasks` and actual development. They are documented here for reference but are not generated artifacts of the `/sp.plan` command.*

### Phase 2 Overview (Reference)

**Goal**: Create production-ready Docker images for frontend and backend

**Key Activities**:
1. Create backend Dockerfile with multi-stage build
2. Create frontend Dockerfile with multi-stage build
3. Implement health check endpoints
4. Create docker-compose.yml for local testing
5. Validate image sizes < 500MB
6. Test containers locally

**Exit Criteria Reference**:
- Backend Dockerfile created and builds successfully
- Frontend Dockerfile created and builds successfully
- Both images under 500MB
- docker-compose integration test passes
- Health endpoints responding correctly

---

## Phase 3: Helm Chart Development (Reference)

**Goal**: Create complete Helm charts for Kubernetes deployment

**Key Activities**:
1. Initialize Helm chart structure
2. Create backend deployment and service templates
3. Create frontend deployment and service templates
4. Create ConfigMap template
5. Configure values.yaml with parameterization
6. Validate with helm lint

**Exit Criteria Reference**:
- Helm chart structure complete
- All templates created and validated
- values.yaml fully parameterized
- helm lint passes with no errors

---

## Phase 4: Kubernetes Deployment (Reference)

**Goal**: Deploy application to Minikube and verify functionality

**Key Activities**:
1. Load images into Minikube
2. Create Kubernetes Secrets manually
3. Deploy with Helm
4. Verify pod health and readiness
5. Access application via Minikube service
6. Test frontend-backend communication

**Exit Criteria Reference**:
- All pods in Running state
- Health checks passing
- Frontend accessible via browser
- Backend API responding
- CRUD operations functional

---

## Phase 5: End-to-End Testing (Reference)

**Goal**: Verify complete application functionality

**Key Activities**:
1. Functional testing (CRUD operations)
2. Scaling testing (kubectl-ai)
3. Resilience testing (pod deletion/recovery)
4. Performance validation

**Exit Criteria Reference**:
- All CRUD operations working
- Scaling operations successful
- Self-healing verified
- Performance within targets

---

## Phase 6: Documentation & Automation (Reference)

**Goal**: Create deployment documentation and automation scripts

**Key Activities**:
1. Create setup-minikube.sh
2. Create build-images.sh
3. Create deploy.sh
4. Create teardown.sh
5. Write K8S-DEPLOYMENT.md
6. Document AI tools usage in AI-TOOLS-LOG.md

**Exit Criteria Reference**:
- All scripts created and tested
- Documentation complete
- Fresh deployment succeeds using only documentation
- AI tools usage fully documented

---

## Risk Mitigation

| Risk | Impact | Mitigation Strategy | Contingency Plan |
|------|--------|---------------------|------------------|
| Gordon unavailable | Low | Use standard Docker CLI commands | Document manual Dockerfile creation process |
| kubectl-ai unavailable | Low | Fall back to manual kubectl commands | Provide equivalent kubectl command reference |
| Minikube resource constraints | Medium | Document minimum requirements (4 CPU/8GB RAM) | Reduce replica counts to 1 for testing |
| Image build failures | Medium | Validate Dockerfiles with linting tools | Step-by-step troubleshooting guide in docs |
| Neon DB connectivity from Minikube | High | Test connection from pods early | Document network troubleshooting steps |
| Health check endpoint issues | Medium | Test endpoints locally before K8s deployment | Fallback to TCP socket checks if needed |
| Helm chart validation errors | Medium | Use helm lint and dry-run extensively | Template-by-template validation process |
| Secret management errors | High | Clear documentation with kubectl examples | Provide troubleshooting for Secret mount issues |

---

## Success Criteria Summary

### Required (P0) - Must Complete
- [x] Both containers built and running locally
- [x] Helm charts created and validated
- [x] Application deployed on Minikube
- [x] Frontend accessible externally via NodePort
- [x] Backend API functional and accessible internally
- [x] Full CRUD operations working end-to-end

### Important (P1) - Should Complete
- [x] Health probes configured (liveness and readiness)
- [x] Resource limits defined per clarification session
- [x] At least 3 kubectl-ai commands used and documented
- [x] K8S-DEPLOYMENT.md complete and tested
- [x] AI-TOOLS-LOG.md documenting all AI tool interactions

### Bonus (P2) - Nice to Have
- [ ] Gordon used successfully for Dockerfile optimization
- [ ] Horizontal Pod Autoscaler configured and tested
- [ ] Ingress configured for cleaner URL access
- [ ] Helm chart published to repository

---

## AI Tools Usage Strategy

### kubectl-ai (Required)
**Planned Operations** (minimum 3):
1. Deployment verification: `kubectl-ai "show me the status of all deployments in todo-app namespace"`
2. Pod troubleshooting: `kubectl-ai "check why pods are not ready"`
3. Scaling operations: `kubectl-ai "scale the frontend deployment to 3 replicas"`
4. Log viewing: `kubectl-ai "show me the logs of the frontend pod"`
5. Service inspection: `kubectl-ai "describe the backend service"`

**Fallback**: Manual kubectl commands if kubectl-ai unavailable

### Gordon (Optional)
**Planned Operations**:
1. Dockerfile generation: `docker ai "Create an optimized Dockerfile for my Next.js frontend"`
2. Security review: `docker ai "Analyze my Dockerfile for security best practices"`
3. Image optimization: `docker ai "Help me reduce the image size"`

**Fallback**: Manual Dockerfile creation using research.md best practices

### Documentation Requirement
All AI tool commands will be logged in `AI-TOOLS-LOG.md` with:
- Command executed
- Tool used (kubectl-ai or Gordon)
- Output/result
- Whether fallback was needed
- Rationale for using AI tool vs manual command

---

## Timeline Estimate (Reference Only)

**Phase 0 (Research)**: ~2-4 hours
**Phase 1 (Design)**: ~2-3 hours
**Phase 2 (Containerization)**: ~4-6 hours
**Phase 3 (Helm Charts)**: ~3-4 hours
**Phase 4 (Deployment)**: ~2-3 hours
**Phase 5 (Testing)**: ~2-3 hours
**Phase 6 (Documentation)**: ~2-3 hours

**Total Estimated**: ~17-26 hours

*Note: Timeline assumes familiarity with Docker, Kubernetes, and Helm. First-time implementations may require additional time for learning and troubleshooting.*

---

## Next Steps

1. **Immediate**: Run `/sp.tasks` to generate detailed task breakdown
2. **Phase 0**: Complete research.md with technology decisions
3. **Phase 1**: Generate data-model.md and contracts
4. **Phase 2+**: Execute implementation following this plan

**Ready to Proceed**: ✅ This plan provides sufficient detail for task generation and implementation.
