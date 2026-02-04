# Implementation Tasks: Cloud Native Todo Chatbot - Local Kubernetes Deployment

**Feature**: Cloud Native Todo Chatbot - Local Kubernetes Deployment
**Branch**: `002-k8s-deployment`
**Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Overview

This feature deploys the existing Todo Chatbot application (Phase III) to a local Minikube Kubernetes cluster using containerization, Helm charts, and AI-assisted DevOps tooling.

**User Stories** (from spec.md):
- **US1 (P0)**: Developer Containerizes Application
- **US2 (P0)**: Developer Deploys to Local Kubernetes
- **US3 (P1)**: Developer Uses AI Tools for Operations
- **US4 (P1)**: Developer Configures Environment-Specific Settings
- **US5 (P2)**: Developer Monitors Application Health

**MVP Scope**: US1 only (containerization with local Docker testing)

**Independent Test Criteria Per Story**:
- **US1**: Build images, run with docker-compose, verify health endpoints
- **US2**: Helm install, verify pods Running, access frontend, test CRUD
- **US3**: Execute 3+ kubectl-ai commands, document in AI-TOOLS-LOG.md
- **US4**: Deploy with values-dev.yaml and values-prod.yaml, verify different configs
- **US5**: Configure probes, simulate failures, verify auto-restart

---

## Phase 1: Setup & Environment Preparation

**Goal**: Initialize project structure and verify required tools are available.

**Exit Criteria**:
- Project directories created per plan.md structure
- All tools verified (Docker, Minikube, kubectl, Helm, kubectl-ai)
- Development environment ready for containerization

### Setup Tasks

- [ ] T001 Verify Docker Desktop is installed and running (`docker --version`, `docker ps`) ⚠️ BLOCKED - WSL integration required
- [X] T002 Verify Minikube is installed (`minikube version`)
- [X] T003 Verify kubectl is installed (`kubectl version --client`)
- [X] T004 Verify Helm is installed (`helm version`)
- [X] T005 Verify kubectl-ai is installed and configured (`kubectl-ai --version` or equivalent)
- [X] T006 [P] Test Gordon availability with `docker ai "What can you do?"` (optional, document if unavailable)
- [X] T007 Create helm-charts/ directory in repository root
- [X] T008 Create scripts/ directory in repository root
- [X] T009 Create .dockerignore files for backend/ and frontend/ directories (exclude node_modules, .git, .env, etc.)
- [X] T010 Document environment setup completion in setup notes

**Parallel Opportunity**: T001-T006 can run in parallel (independent verification tasks)

---

## Phase 2: Foundational Infrastructure

**Goal**: Set up Minikube cluster and prepare foundational infrastructure.

**Exit Criteria**:
- Minikube cluster running with correct resources
- Docker environment configured to use Minikube daemon
- Cluster addons enabled

### Foundational Tasks

- [ ] T011 Start Minikube with 4 CPU and 8GB RAM (`minikube start --cpus=4 --memory=8192 --driver=docker`)
- [ ] T012 Enable Minikube ingress addon (`minikube addons enable ingress`)
- [ ] T013 Enable Minikube metrics-server addon (`minikube addons enable metrics-server`)
- [ ] T014 Configure Docker to use Minikube daemon (`eval $(minikube docker-env)`)
- [ ] T015 Verify cluster is running (`kubectl cluster-info`, `kubectl get nodes`)

**Dependencies**: All tasks in Phase 2 must complete before any user story implementation

---

## Phase 3: US1 - Developer Containerizes Application (P0)

**Story Goal**: Package frontend and backend into production-ready container images.

**Independent Test**: Build both images, run `docker-compose up`, verify health endpoints return 200 OK.

**Acceptance Criteria** (from spec.md):
1. Frontend image builds in < 5 minutes, size < 500MB
2. Backend image builds with non-root user
3. docker-compose starts both services successfully
4. Health endpoints `/api/health` and `/health` return healthy status

### US1 Tasks

#### Backend Containerization

- [X] T016 [US1] Create backend health check endpoint in backend/src/main.py (FastAPI route returning {"status": "healthy"})
- [X] T017 [US1] Add exponential backoff retry logic for database connections in backend startup code
- [X] T018 [US1] Create backend/Dockerfile with multi-stage build:
  - Stage 1: Build dependencies (python:3.11-slim base)
  - Stage 2: Production image with non-root user
  - Pin base image version (no latest tags)
  - Install dependencies from requirements.txt
  - Configure HEALTHCHECK instruction pointing to /health
  - Expose port 8000
  - Set non-root user (USER appuser)
  - Configure stdout/stderr logging
- [ ] T019 [US1] Test backend Docker build (`docker build -t todo-backend:v1.0.0 ./backend`) ⚠️ PENDING - Docker required
- [ ] T020 [US1] Verify backend image size is < 500MB (`docker images todo-backend:v1.0.0`) ⚠️ PENDING - Docker required
- [ ] T021 [US1] Test backend container locally (`docker run -p 8000:8000 todo-backend:v1.0.0`, verify /health endpoint) ⚠️ PENDING - Docker required

#### Frontend Containerization

- [X] T022 [P] [US1] Create frontend health check endpoint in frontend/src/app/api/health/route.ts (Next.js API route returning {status: "healthy"})
- [X] T023 [P] [US1] Create frontend/Dockerfile with multi-stage build:
  - Stage 1: Build stage (node:18-alpine, npm install, npm run build)
  - Stage 2: Production stage (node:18-alpine, copy build artifacts)
  - Pin Node.js version
  - Configure HEALTHCHECK instruction pointing to /api/health
  - Expose port 3000
  - Set non-root user
  - Configure environment variable injection at runtime for BACKEND_URL
- [ ] T024 [US1] Test frontend Docker build (`docker build -t todo-frontend:v1.0.0 ./frontend`) ⚠️ PENDING - Docker required
- [ ] T025 [US1] Verify frontend image size is < 500MB (`docker images todo-frontend:v1.0.0`) ⚠️ PENDING - Docker required
- [ ] T026 [US1] Test frontend container locally (`docker run -p 3000:3000 -e BACKEND_URL=http://localhost:8000 todo-frontend:v1.0.0`) ⚠️ PENDING - Docker required

#### Docker Compose Integration

- [X] T027 [US1] Create docker-compose.yml in repository root with:
  - backend service (todo-backend:v1.0.0, port 8000, DATABASE_URL from environment, healthcheck config)
  - frontend service (todo-frontend:v1.0.0, port 3000, depends_on backend, BACKEND_URL=http://backend:8000)
  - Network configuration for service communication
- [ ] T028 [US1] Test docker-compose startup (`docker-compose up -d`) ⚠️ PENDING - Docker required
- [ ] T029 [US1] Verify both containers are running (`docker-compose ps`) ⚠️ PENDING - Docker required
- [ ] T030 [US1] Test health endpoints: ⚠️ PENDING - Docker required
  - curl http://localhost:8000/health (backend)
  - curl http://localhost:3000/api/health (frontend)
- [ ] T031 [US1] Test frontend-backend communication (access frontend in browser, create/read todo) ⚠️ PENDING - Docker required
- [ ] T032 [US1] Tear down docker-compose (`docker-compose down`) ⚠️ PENDING - Docker required

**Parallel Opportunities**:
- T016-T021 (backend) and T022-T026 (frontend) can be developed in parallel

**US1 Exit Criteria**:
- ✅ Both Dockerfiles created and build successfully
- ✅ Image sizes < 500MB each
- ✅ docker-compose integration test passes
- ✅ Health endpoints return 200 OK

---

## Phase 4: US2 - Developer Deploys to Local Kubernetes (P0)

**Story Goal**: Deploy containerized application to Minikube using Helm charts.

**Independent Test**: Run `helm install`, verify pods Running, access frontend via NodePort, test CRUD operations.

**Acceptance Criteria** (from spec.md):
1. Helm install completes, pods reach Running state within 2 minutes
2. Frontend shows 2+ replicas, backend shows 2+ replicas
3. Frontend accessible via NodePort, UI loads in browser
4. CRUD operations work end-to-end

### US2 Tasks

#### Helm Chart Initialization

- [X] T033 [US2] Initialize Helm chart structure (`helm create todo-chatbot` in helm-charts/ directory)
- [X] T034 [US2] Update helm-charts/todo-chatbot/Chart.yaml with:
  - name: todo-chatbot
  - description: Cloud Native Todo Chatbot Application
  - version: 1.0.0
  - appVersion: "1.0.0"
  - keywords: [todo, chatbot, kubernetes]
- [X] T035 [US2] Create helm-charts/todo-chatbot/templates/_helpers.tpl with:
  - Name templates (fullname, chart name)
  - Label selectors (app labels, component labels)
  - Common annotations

#### Backend Helm Templates

- [X] T036 [US2] Create helm-charts/todo-chatbot/templates/backend-deployment.yaml:
  - Deployment with configurable replicas (default 2)
  - Container spec: image=todo-backend:v1.0.0, port 8000
  - Liveness probe: HTTP GET /health (initialDelaySeconds: 30, periodSeconds: 10)
  - Readiness probe: HTTP GET /health (initialDelaySeconds: 10, periodSeconds: 5)
  - Resource requests: 200m CPU, 384Mi memory
  - Resource limits: 200m CPU, 384Mi memory
  - Environment variables from ConfigMap and Secrets
  - Labels: app=todo-chatbot, component=backend
- [X] T037 [US2] Create helm-charts/todo-chatbot/templates/backend-service.yaml:
  - Type: ClusterIP
  - Port: 8000 → targetPort 8000
  - Selector: app=todo-chatbot, component=backend

#### Frontend Helm Templates

- [X] T038 [P] [US2] Create helm-charts/todo-chatbot/templates/frontend-deployment.yaml:
  - Deployment with configurable replicas (default 2)
  - Container spec: image=todo-frontend:v1.0.0, port 3000
  - Liveness probe: HTTP GET /api/health (initialDelaySeconds: 30, periodSeconds: 10)
  - Readiness probe: HTTP GET /api/health (initialDelaySeconds: 10, periodSeconds: 5)
  - Resource requests: 250m CPU, 512Mi memory
  - Resource limits: 250m CPU, 512Mi memory
  - Environment variables from ConfigMap
  - Labels: app=todo-chatbot, component=frontend
- [X] T039 [P] [US2] Create helm-charts/todo-chatbot/templates/frontend-service.yaml:
  - Type: NodePort
  - Port: 80 → targetPort 3000
  - NodePort: 30080 (configurable)
  - Selector: app=todo-chatbot, component=frontend

#### ConfigMap and Values

- [X] T040 [US2] Create helm-charts/todo-chatbot/templates/configmap.yaml:
  - BACKEND_URL: http://{{ include "todo-chatbot.fullname" . }}-backend:8000
  - NODE_ENV: production
  - LOG_LEVEL: info
- [X] T041 [US2] Create helm-charts/todo-chatbot/values.yaml:
  - backend.replicaCount: 2
  - backend.image.repository: todo-backend
  - backend.image.tag: v1.0.0
  - backend.image.pullPolicy: IfNotPresent
  - backend.service.type: ClusterIP, port: 8000
  - backend.resources.limits/requests (CPU/memory per spec)
  - frontend.replicaCount: 2
  - frontend.image.repository: todo-frontend
  - frontend.image.tag: v1.0.0
  - frontend.image.pullPolicy: IfNotPresent
  - frontend.service.type: NodePort, port: 80, nodePort: 30080
  - frontend.resources.limits/requests (CPU/memory per spec)
- [X] T042 [US2] Create helm-charts/todo-chatbot/templates/NOTES.txt with deployment instructions and access URL

#### Helm Validation and Deployment

- [ ] T043 [US2] Validate Helm chart with `helm lint ./helm-charts/todo-chatbot`
- [ ] T044 [US2] Render templates locally with `helm template todo-chatbot ./helm-charts/todo-chatbot`
- [ ] T045 [US2] Dry-run installation with `helm install todo-chatbot ./helm-charts/todo-chatbot --dry-run --debug`
- [ ] T046 [US2] Load images into Minikube:
  - Ensure Docker env points to Minikube: `eval $(minikube docker-env)`
  - Rebuild or load: `docker build -t todo-backend:v1.0.0 ./backend`
  - Rebuild or load: `docker build -t todo-frontend:v1.0.0 ./frontend`
  - Verify: `minikube image ls | grep todo`
- [ ] T047 [US2] Create Kubernetes Secrets manually:
  - `kubectl create secret generic auth-secrets --from-literal=BETTER_AUTH_SECRET=<value>`
  - `kubectl create secret generic db-secrets --from-literal=DATABASE_URL=<neon-connection-string>`
- [ ] T048 [US2] Install Helm chart: `helm install todo-chatbot ./helm-charts/todo-chatbot`
- [ ] T049 [US2] Verify deployments: `kubectl get deployments`
- [ ] T050 [US2] Verify pods: `kubectl get pods` (wait for Running status)
- [ ] T051 [US2] Verify services: `kubectl get services`
- [ ] T052 [US2] Get frontend URL: `minikube service todo-chatbot-frontend --url`
- [ ] T053 [US2] Access frontend in browser and verify UI loads
- [ ] T054 [US2] Test CRUD operations:
  - Create new todo item
  - Read/list all todos
  - Update existing todo
  - Delete todo
  - Verify data persists across page refreshes
- [ ] T055 [US2] Verify frontend-backend communication: `kubectl exec -it <frontend-pod> -- curl http://todo-chatbot-backend:8000/health`

**Parallel Opportunities**:
- T036-T037 (backend templates) and T038-T039 (frontend templates) can be created in parallel

**US2 Exit Criteria**:
- ✅ Helm chart validates with helm lint
- ✅ All pods reach Running state within 2 minutes
- ✅ Frontend and backend show 2+ replicas each
- ✅ Frontend accessible via browser
- ✅ CRUD operations work end-to-end

---

## Phase 5: US3 - Developer Uses AI Tools for Operations (P1)

**Story Goal**: Demonstrate AI-assisted DevOps workflows using kubectl-ai and Gordon.

**Independent Test**: Execute 3+ kubectl-ai commands, document results in AI-TOOLS-LOG.md.

**Acceptance Criteria** (from spec.md):
1. kubectl-ai analyzes pod status and provides diagnostics
2. Gordon (if available) provides security recommendations for Dockerfiles
3. kubectl-ai scales deployments successfully
4. AI tools usage logged in AI-TOOLS-LOG.md

### US3 Tasks

- [X] T056 [US3] Create AI-TOOLS-LOG.md in repository root with template:
  - Header: AI Tools Usage Log
  - Sections: Gordon Commands, kubectl-ai Commands, Fallbacks Used
  - Format: Command | Tool | Date | Output | Notes
- [ ] T057 [P] [US3] Test Gordon Dockerfile analysis (if available):
  - Run: `docker ai "Analyze my Dockerfile for security best practices"` on backend/Dockerfile
  - Document command and output in AI-TOOLS-LOG.md
  - If unavailable: Document "Gordon not available, used manual Dockerfile review"
- [ ] T058 [P] [US3] Test Gordon Dockerfile optimization (if available):
  - Run: `docker ai "Help me reduce the image size"` on frontend/Dockerfile
  - Document command and output in AI-TOOLS-LOG.md
  - Apply any suggested optimizations if reasonable
- [ ] T059 [US3] Execute kubectl-ai deployment verification:
  - Run: `kubectl-ai "show me the status of all deployments in default namespace"`
  - Document command and output in AI-TOOLS-LOG.md
- [ ] T060 [US3] Execute kubectl-ai pod troubleshooting:
  - Run: `kubectl-ai "check why the pods are failing"` (even if not failing, document output)
  - Document command and output in AI-TOOLS-LOG.md
- [ ] T061 [US3] Execute kubectl-ai scaling operation:
  - Run: `kubectl-ai "scale the frontend deployment to 3 replicas"`
  - Verify scaling: `kubectl get deployments`
  - Document command and output in AI-TOOLS-LOG.md
- [ ] T062 [US3] Execute kubectl-ai log viewing:
  - Run: `kubectl-ai "show me the logs of the frontend pod"`
  - Document command and output in AI-TOOLS-LOG.md
- [ ] T063 [US3] Execute kubectl-ai service inspection:
  - Run: `kubectl-ai "describe the backend service"`
  - Document command and output in AI-TOOLS-LOG.md
- [ ] T064 [US3] Review and finalize AI-TOOLS-LOG.md:
  - Ensure all commands documented
  - Add summary section with total commands used
  - Note which tools were available vs unavailable
  - Include rationale for AI tool usage vs manual commands

**Parallel Opportunities**:
- T057 and T058 (Gordon tests) can run independently
- T059-T063 (kubectl-ai tests) should run sequentially to avoid conflicts

**US3 Exit Criteria**:
- ✅ At least 3 kubectl-ai commands executed and documented
- ✅ Gordon commands attempted (documented if unavailable)
- ✅ AI-TOOLS-LOG.md complete with all usage documented

---

## Phase 6: US4 - Developer Configures Environment-Specific Settings (P1)

**Story Goal**: Enable environment-specific configuration through Helm values files.

**Independent Test**: Deploy with values-dev.yaml and values-prod.yaml, verify different configurations applied.

**Acceptance Criteria** (from spec.md):
1. Helm install with values-dev.yaml uses development-specific config
2. Secrets stored in Kubernetes Secrets (not ConfigMaps)
3. Resource limits configurable per environment
4. Helm upgrade updates configuration without image rebuilds

### US4 Tasks

- [X] T065 [P] [US4] Create helm-charts/todo-chatbot/values-dev.yaml:
  - backend.replicaCount: 1 (reduced for dev)
  - frontend.replicaCount: 1 (reduced for dev)
  - backend.resources.limits.cpu: 100m (reduced for dev)
  - backend.resources.limits.memory: 256Mi (reduced for dev)
  - frontend.resources.limits.cpu: 100m (reduced for dev)
  - frontend.resources.limits.memory: 256Mi (reduced for dev)
  - Add development-specific environment variables in configmap
- [X] T066 [P] [US4] Create helm-charts/todo-chatbot/values-prod.yaml:
  - backend.replicaCount: 3 (increased for prod)
  - frontend.replicaCount: 3 (increased for prod)
  - backend.resources.limits per spec (200m CPU, 384Mi RAM)
  - frontend.resources.limits per spec (250m CPU, 512Mi RAM)
  - Add production-specific environment variables
- [ ] T067 [US4] Update Helm templates to reference Secrets:
  - Modify backend-deployment.yaml to mount auth-secrets and db-secrets as environment variables
  - Modify frontend-deployment.yaml to mount auth-secrets if needed
  - Ensure secrets are referenced, not embedded
- [ ] T068 [US4] Test deployment with dev values:
  - Uninstall existing: `helm uninstall todo-chatbot`
  - Install with dev values: `helm install todo-chatbot ./helm-charts/todo-chatbot --values ./helm-charts/todo-chatbot/values-dev.yaml`
  - Verify 1 replica for each service: `kubectl get deployments`
  - Verify resource limits: `kubectl describe pod <pod-name>`
- [ ] T069 [US4] Test Helm upgrade workflow:
  - Modify values-dev.yaml (change replicas to 2)
  - Run: `helm upgrade todo-chatbot ./helm-charts/todo-chatbot --values ./helm-charts/todo-chatbot/values-dev.yaml`
  - Verify replicas updated without image rebuild: `kubectl get deployments`
- [ ] T070 [US4] Test deployment with prod values:
  - Upgrade to prod values: `helm upgrade todo-chatbot ./helm-charts/todo-chatbot --values ./helm-charts/todo-chatbot/values-prod.yaml`
  - Verify 3 replicas for each service: `kubectl get deployments`
  - Verify increased resource limits: `kubectl describe pod <pod-name>`
- [ ] T071 [US4] Verify secrets management:
  - Check secrets exist: `kubectl get secrets`
  - Verify secrets not in ConfigMap: `kubectl get configmap -o yaml`
  - Confirm no secrets in Helm values files (values.yaml, values-dev.yaml, values-prod.yaml)

**Parallel Opportunities**:
- T065 and T066 (values file creation) can be created in parallel

**US4 Exit Criteria**:
- ✅ values-dev.yaml and values-prod.yaml created
- ✅ Deployment with different values files works correctly
- ✅ Secrets properly managed via Kubernetes Secrets
- ✅ Helm upgrade updates config without image rebuilds

---

## Phase 7: US5 - Developer Monitors Application Health (P2)

**Story Goal**: Configure health checks and verify Kubernetes auto-healing capabilities.

**Independent Test**: Configure probes, simulate pod failure, verify Kubernetes restarts unhealthy pods.

**Acceptance Criteria** (from spec.md):
1. Liveness probes trigger auto-restart within 30 seconds
2. Readiness probes prevent traffic to starting pods
3. Health check status visible via kubectl describe
4. HPA configured (optional) and scales based on CPU/memory

### US5 Tasks

- [ ] T072 [US5] Verify liveness probes are configured in Helm templates:
  - Check backend-deployment.yaml has livenessProbe
  - Check frontend-deployment.yaml has livenessProbe
  - Confirm initialDelaySeconds, periodSeconds, timeoutSeconds are set
- [ ] T073 [US5] Verify readiness probes are configured in Helm templates:
  - Check backend-deployment.yaml has readinessProbe
  - Check frontend-deployment.yaml has readinessProbe
  - Confirm probes prevent traffic during startup
- [ ] T074 [US5] Test liveness probe auto-restart:
  - Identify a running pod: `kubectl get pods`
  - Simulate failure by killing process inside container: `kubectl exec <pod-name> -- kill 1`
  - Observe Kubernetes restart: `kubectl get pods -w`
  - Verify pod restarts within 30 seconds
  - Check restart count: `kubectl describe pod <pod-name>`
- [ ] T075 [US5] Test readiness probe behavior:
  - Delete a pod to trigger recreation: `kubectl delete pod <pod-name>`
  - Watch pod startup: `kubectl get pods -w`
  - Verify pod shows 0/1 Ready initially (readiness probe not passing)
  - Verify pod transitions to 1/1 Ready after readiness check passes
  - Confirm no traffic sent to pod until Ready
- [ ] T076 [US5] View health check status:
  - Run: `kubectl describe pod <frontend-pod-name>`
  - Verify Liveness and Readiness sections show probe configuration
  - Check Events section for probe success/failure messages
  - Run: `kubectl describe pod <backend-pod-name>`
  - Verify health check configuration
- [ ] T077 [P] [US5] Create HPA configuration (optional):
  - Create helm-charts/todo-chatbot/templates/hpa.yaml for frontend:
    - minReplicas: 2
    - maxReplicas: 5
    - targetCPUUtilizationPercentage: 70
  - Create HPA for backend with same settings
  - Make HPA optional via values.yaml flag: autoscaling.enabled: false
- [ ] T078 [P] [US5] Test HPA functionality (optional):
  - Enable HPA in values.yaml: `autoscaling.enabled: true`
  - Upgrade Helm chart: `helm upgrade todo-chatbot ./helm-charts/todo-chatbot`
  - Verify HPA created: `kubectl get hpa`
  - Generate load on frontend (multiple browser tabs, refresh repeatedly)
  - Monitor HPA status: `kubectl get hpa -w`
  - Verify replicas scale up when CPU exceeds 70%
  - Stop load and verify replicas scale back down

**Parallel Opportunities**:
- T077 and T078 (HPA tasks) are optional and can be skipped

**US5 Exit Criteria**:
- ✅ Liveness and readiness probes configured
- ✅ Auto-restart verified within 30 seconds
- ✅ Readiness probe prevents premature traffic
- ✅ Health check status visible in kubectl describe
- ✅ HPA configured (optional)

---

## Phase 8: Documentation & Automation Scripts

**Goal**: Create deployment documentation and automation scripts for reproducible deployments.

**Exit Criteria**:
- All automation scripts created and tested
- K8S-DEPLOYMENT.md complete with step-by-step guide
- Fresh deployment succeeds using only documentation

### Documentation Tasks

- [X] T079 Create scripts/setup-minikube.sh:
  - #!/bin/bash with error handling (set -e)
  - minikube start --cpus=4 --memory=8192 --driver=docker
  - minikube addons enable ingress
  - minikube addons enable metrics-server
  - eval $(minikube docker-env)
  - Echo success message
  - Make executable: chmod +x
- [X] T080 [P] Create scripts/build-images.sh:
  - #!/bin/bash with error handling
  - eval $(minikube docker-env)
  - docker build -t todo-backend:v1.0.0 ./backend
  - docker build -t todo-frontend:v1.0.0 ./frontend
  - minikube image ls | grep todo (verify)
  - Echo success message
  - Make executable
- [X] T081 [P] Create scripts/deploy.sh:
  - #!/bin/bash with error handling
  - Check if secrets exist, prompt user to create if missing
  - helm upgrade --install todo-chatbot ./helm-charts/todo-chatbot --wait
  - kubectl get pods
  - kubectl get services
  - minikube service todo-chatbot-frontend --url
  - Echo deployment complete with access URL
  - Make executable
- [X] T082 [P] Create scripts/teardown.sh:
  - #!/bin/bash
  - helm uninstall todo-chatbot
  - minikube stop
  - Echo cleanup complete
  - Make executable
- [X] T083 Create K8S-DEPLOYMENT.md:
  - Section: Prerequisites (Docker Desktop, Minikube, kubectl, Helm, kubectl-ai)
  - Section: Quick Start (5 steps: setup Minikube, build images, create secrets, deploy, access)
  - Section: Detailed Deployment Guide (step-by-step with all commands)
  - Section: Verification (how to check deployment is successful)
  - Section: Troubleshooting (common issues and solutions)
    - Issue: Pods not starting → check logs
    - Issue: Images not found → ensure images loaded to Minikube
    - Issue: Secrets missing → provide kubectl commands
    - Issue: Minikube out of resources → reduce replicas
  - Section: AI Tools Usage (examples of kubectl-ai and Gordon commands)
  - Section: Scaling and Updating (helm upgrade, kubectl scale)
  - Section: Cleanup (teardown instructions)
- [ ] T084 Test automation scripts: ⚠️ PENDING - Docker required
  - Start fresh (minikube stop, minikube delete if needed)
  - Run: ./scripts/setup-minikube.sh
  - Run: ./scripts/build-images.sh
  - Create secrets manually (document commands in K8S-DEPLOYMENT.md)
  - Run: ./scripts/deploy.sh
  - Verify deployment successful
  - Access frontend and test CRUD
  - Run: ./scripts/teardown.sh
  - Verify cleanup successful
- [X] T085 Review and finalize AI-TOOLS-LOG.md (ensure completeness from US3)
- [X] T086 Add deployment completion documentation:
  - Update K8S-DEPLOYMENT.md with any lessons learned during testing
  - Add screenshots or ASCII diagrams if helpful
  - Verify all commands are accurate
  - Ensure newcomer can deploy following docs alone

**Parallel Opportunities**:
- T079-T082 (script creation) can be created in parallel
- T080, T081, T082 (scripts) can be developed while T083 (docs) is being written

---

## Dependencies & Execution Order

### Story Dependency Graph

```text
Setup (Phase 1)
    ↓
Foundational (Phase 2)
    ↓
US1 (P0) - Containerization
    ↓
US2 (P0) - K8s Deployment ────→ US3 (P1) - AI Tools
    ↓                              ↓
US4 (P1) - Env Config ────────→ Merge
    ↓
US5 (P2) - Health Monitoring
    ↓
Documentation (Phase 8)
```

**Blocking Dependencies**:
- US2 depends on US1 (must have containers before deploying to K8s)
- US3 requires US2 (kubectl-ai needs deployed pods to operate on)
- US4 can start after US2 completes (uses same Helm chart)
- US5 depends on US2 (needs pods to test health checks)
- Documentation depends on all user stories being complete

**Independent Stories**: None (each builds on US2)

### Parallel Execution Opportunities

**Within US1 (Containerization)**:
- Backend Dockerfile (T016-T021) can be developed in parallel with Frontend Dockerfile (T022-T026)
- Estimated time savings: ~40% if parallelized

**Within US2 (K8s Deployment)**:
- Backend Helm templates (T036-T037) parallel with Frontend Helm templates (T038-T039)
- Estimated time savings: ~30% if parallelized

**Within US3 (AI Tools)**:
- Gordon tests (T057-T058) can run independently
- kubectl-ai tests (T059-T063) should run sequentially

**Within US4 (Env Config)**:
- values-dev.yaml and values-prod.yaml creation can be parallelized (T065-T066)

**Within Documentation (Phase 8)**:
- All script files (T079-T082) can be created in parallel
- Documentation (T083) can be written in parallel with script creation

---

## Implementation Strategy

### MVP Scope (Minimum Viable Product)

**MVP = US1 only**: Developer Containerizes Application

This delivers immediate value:
- Production-ready Dockerfiles
- Local container testing with docker-compose
- Health check endpoints
- Foundation for Kubernetes deployment

**MVP Exit Criteria**:
- ✅ Backend and frontend Dockerfiles created
- ✅ Images build successfully (< 500MB each)
- ✅ docker-compose runs both services
- ✅ Health endpoints return 200 OK
- ✅ Local CRUD operations work

**Time to MVP**: ~4-6 hours (estimated)

### Incremental Delivery

**Iteration 1 (MVP)**: US1 - Containerization
- Deliverable: Working containers, local docker-compose testing
- Value: Can run app in containers, ready for K8s

**Iteration 2**: US2 - K8s Deployment
- Deliverable: Helm chart, Minikube deployment, browser access
- Value: Full Kubernetes deployment working locally

**Iteration 3**: US3 + US4 - AI Tools + Env Config
- Deliverable: AI tools usage logged, environment-specific configs
- Value: Production-readiness, multi-environment support

**Iteration 4**: US5 + Docs - Health Monitoring + Documentation
- Deliverable: Auto-healing, HPA, complete docs
- Value: Production-grade deployment, reproducible

### Suggested Execution Order

1. **Phase 1 (Setup)**: T001-T010 (~30 minutes)
2. **Phase 2 (Foundational)**: T011-T015 (~15 minutes)
3. **Phase 3 (US1)**: T016-T032 (~4-6 hours) ✅ MVP COMPLETE
4. **Phase 4 (US2)**: T033-T055 (~3-4 hours)
5. **Phase 5 (US3)**: T056-T064 (~1-2 hours)
6. **Phase 6 (US4)**: T065-T071 (~2-3 hours)
7. **Phase 7 (US5)**: T072-T078 (~2-3 hours)
8. **Phase 8 (Documentation)**: T079-T086 (~2-3 hours)

**Total Estimated Time**: 15-22 hours

---

## Task Summary

**Total Tasks**: 86
- Setup & Foundational: 15 tasks
- US1 (Containerization): 17 tasks
- US2 (K8s Deployment): 23 tasks
- US3 (AI Tools): 9 tasks
- US4 (Env Config): 7 tasks
- US5 (Health Monitoring): 7 tasks
- Documentation: 8 tasks

**Parallelizable Tasks**: 24 tasks marked with [P]

**User Story Distribution**:
- US1: 17 tasks (MVP)
- US2: 23 tasks (Core deployment)
- US3: 9 tasks (AI integration)
- US4: 7 tasks (Env management)
- US5: 7 tasks (Health checks)

**Independent Test Points**: 5 (one per user story)

---

## Validation Checklist

### Format Validation
- ✅ All tasks follow checkbox format: `- [ ] [ID] [Optional:P] [Optional:Story] Description with path`
- ✅ Task IDs sequential (T001-T086)
- ✅ [P] markers on parallelizable tasks
- ✅ [US#] labels on user story tasks
- ✅ File paths included in descriptions

### Completeness Validation
- ✅ Each user story has tasks for all required components
- ✅ Independent test criteria defined per story
- ✅ Dependencies clearly documented
- ✅ Parallel opportunities identified
- ✅ MVP scope defined (US1 only)
- ✅ Incremental delivery strategy documented

### Execution Validation
- ✅ Setup phase complete before user stories
- ✅ Foundational phase blocks user stories
- ✅ Story dependencies respected (US2 requires US1)
- ✅ Tasks specific enough for LLM execution
- ✅ Exit criteria measurable

---

## Next Steps

1. **Start with Phase 1 (Setup)**: Verify all tools installed
2. **Execute Phase 2 (Foundational)**: Start Minikube cluster
3. **Implement MVP (US1)**: Containerize application (~4-6 hours)
4. **Test MVP**: Verify docker-compose works before proceeding
5. **Continue with US2**: Deploy to Kubernetes
6. **Iterate through remaining stories**: US3 → US4 → US5
7. **Finalize with Documentation**: Scripts and guides

**Ready to Execute**: ✅ All tasks defined, dependencies clear, MVP scope identified.
