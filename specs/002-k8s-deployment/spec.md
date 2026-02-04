# Feature Specification: Cloud Native Todo Chatbot - Local Kubernetes Deployment

**Feature Branch**: `002-k8s-deployment`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Cloud Native Todo Chatbot - Local Kubernetes Deployment"

## Clarifications

### Session 2026-01-25
- Q: What health check endpoint pattern should be used for liveness and readiness probes? → A: Framework-specific health checks (Next.js API route `/api/health`, FastAPI `/health`)
- Q: What logging strategy should containers use for observability and debugging? → A: Log to stdout/stderr (container standard)
- Q: What CPU and memory resource limits should be set for frontend and backend pods? → A: Moderate: Frontend (250m CPU, 512Mi RAM), Backend (200m CPU, 384Mi RAM)
- Q: How should pods handle startup failures (e.g., database connection failures)? → A: Retry with exponential backoff
- Q: What rollback strategy should be used if a Helm deployment fails? → A: Manual rollback on failure

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Containerizes Application (Priority: P0)

A developer needs to package the existing Todo Chatbot application (frontend and backend) into production-ready container images that can run consistently across different environments.

**Why this priority**: This is the foundational step - without containerized applications, Kubernetes deployment is impossible. This represents the first deliverable and enables local testing with Docker Compose.

**Independent Test**: Can be fully tested by building both Docker images successfully, running them locally with `docker run`, and verifying that both containers start without errors and respond to health checks. Delivers the ability to run the application in containers independent of Kubernetes.

**Acceptance Scenarios**:

1. **Given** the frontend application source code, **When** developer builds the frontend Dockerfile, **Then** the image builds successfully in under 5 minutes with size under 500MB
2. **Given** the backend application source code, **When** developer builds the backend Dockerfile, **Then** the image builds successfully with non-root user configuration
3. **Given** both container images are built, **When** developer runs `docker-compose up`, **Then** both services start and can communicate with each other locally
4. **Given** containers are running, **When** health check endpoints are queried, **Then** both services return healthy status

---

### User Story 2 - Developer Deploys to Local Kubernetes (Priority: P0)

A developer needs to deploy the containerized Todo Chatbot application to a local Minikube cluster using Helm charts, making it accessible via browser for testing.

**Why this priority**: This is the core deliverable - getting the application running in Kubernetes. Without this, the deployment objectives are not met.

**Independent Test**: Can be fully tested by running Helm install commands, verifying pod status with kubectl, and accessing the frontend through NodePort or Minikube tunnel. Delivers a working Kubernetes deployment that demonstrates container orchestration capabilities.

**Acceptance Scenarios**:

1. **Given** Minikube is running with 4 CPU and 8GB RAM, **When** developer runs `helm install todo-chatbot ./helm-charts/todo-chatbot`, **Then** all pods reach Running state within 2 minutes
2. **Given** the Helm deployment is complete, **When** developer checks pod status, **Then** frontend shows 2+ replicas running and backend shows 2+ replicas running
3. **Given** pods are running, **When** developer accesses the frontend via NodePort URL, **Then** the Todo Chatbot UI loads in the browser
4. **Given** the UI is loaded, **When** user creates a new todo item, **Then** the item is saved via backend API and persists across page refreshes

---

### User Story 3 - Developer Uses AI Tools for Operations (Priority: P1)

A developer wants to leverage AI-assisted DevOps tools (kubectl-ai and optionally Gordon) to streamline Docker and Kubernetes operations through natural language commands.

**Why this priority**: This demonstrates modern AI-assisted workflows and reduces the learning curve for Kubernetes operations. It's not essential for basic deployment but significantly improves developer experience.

**Independent Test**: Can be fully tested by executing at least 3 kubectl-ai commands (e.g., checking pod status, scaling deployments, viewing logs) and documenting the commands used and results. Delivers productivity improvements and demonstrates AI tool integration.

**Acceptance Scenarios**:

1. **Given** kubectl-ai is installed, **When** developer runs `kubectl-ai "check why the pods are failing"`, **Then** the tool analyzes pod status and provides diagnostic information
2. **Given** Gordon is available, **When** developer runs `docker ai "Analyze my Dockerfile for security best practices"`, **Then** the tool provides security recommendations
3. **Given** deployments are running, **When** developer runs `kubectl-ai "scale the backend to handle more load"`, **Then** the backend replica count increases appropriately
4. **Given** AI tool operations are executed, **When** deployment is complete, **Then** an AI tools usage log documents all commands used

---

### User Story 4 - Developer Configures Environment-Specific Settings (Priority: P1)

A developer needs to manage configuration and secrets separately from application code, supporting different environments (dev, staging, prod) through Helm values.

**Why this priority**: This ensures security best practices (no hardcoded secrets) and deployment flexibility. Required for production-readiness but not blocking for initial local deployment.

**Independent Test**: Can be fully tested by deploying with different values files (`values-dev.yaml`, `values-prod.yaml`), verifying ConfigMaps contain correct environment variables, and confirming secrets are properly mounted. Delivers environment configuration management independent of core deployment.

**Acceptance Scenarios**:

1. **Given** Helm chart with parameterized values.yaml, **When** developer runs `helm install --values values-dev.yaml`, **Then** pods use development-specific configuration
2. **Given** sensitive data like database credentials exist, **When** deployment occurs, **Then** secrets are stored in Kubernetes Secrets (not ConfigMaps or hardcoded)
3. **Given** different resource requirements for environments, **When** developer specifies resource limits in values file, **Then** pods are scheduled with correct CPU and memory limits
4. **Given** configuration changes are needed, **When** developer updates values.yaml and runs `helm upgrade`, **Then** configuration updates without requiring image rebuilds

---

### User Story 5 - Developer Monitors Application Health (Priority: P2)

A developer needs to verify that the deployed application is healthy and performing correctly through Kubernetes health checks and monitoring.

**Why this priority**: Health checks ensure reliability and enable automatic recovery, but the application can function without them initially. This is important for production readiness but not blocking for initial deployment.

**Independent Test**: Can be fully tested by configuring liveness and readiness probes, then simulating failures (e.g., killing a process) and verifying Kubernetes automatically restarts unhealthy pods. Delivers automated health monitoring and self-healing capabilities.

**Acceptance Scenarios**:

1. **Given** liveness probes are configured, **When** a pod becomes unhealthy, **Then** Kubernetes automatically restarts the pod within 30 seconds
2. **Given** readiness probes are configured, **When** a pod is starting up, **Then** it doesn't receive traffic until the readiness check passes
3. **Given** pods are running, **When** developer checks deployment status, **Then** health check status is visible via kubectl describe
4. **Given** load increases, **When** Horizontal Pod Autoscaler (HPA) is configured, **Then** replicas scale automatically based on CPU/memory metrics

---

### Edge Cases

- What happens when Minikube runs out of resources (CPU/memory limits reached)?
- How does the system handle image pull failures when loading images into Minikube?
- **Database connection failures during startup**: Backend application MUST implement exponential backoff retry logic (e.g., retry after 1s, 2s, 4s, 8s, 16s). After maximum retry attempts (e.g., 5-10 attempts), pod enters Failed state and Kubernetes restart policy takes over. Application MUST log each retry attempt with connection details (excluding credentials) for debugging.
- **Pod crashes after passing health checks**: Kubernetes liveness probe detects unhealthy state and automatically restarts the pod. Application state is not preserved (stateless design).
- What happens when ConfigMap or Secret changes require pod restarts?
- **Network connectivity issues between frontend and backend**: Frontend should display user-friendly error messages when backend API calls fail. Kubernetes DNS ensures service discovery works; if backend pods are down, requests timeout per service configuration.
- What occurs if Helm chart validation fails during deployment (e.g., invalid YAML)?

## Requirements *(mandatory)*

### Functional Requirements

#### Containerization
- **FR-001**: Frontend application MUST be containerized using a multi-stage Dockerfile that minimizes final image size to under 500MB
- **FR-002**: Backend application MUST be containerized using a Dockerfile that runs as non-root user
- **FR-003**: Both container images MUST include health check instructions (HEALTHCHECK directive or equivalent). Frontend MUST expose `/api/health` endpoint (Next.js API route). Backend MUST expose `/health` endpoint (FastAPI route). Both endpoints MUST return HTTP 200 status when healthy.
- **FR-004**: Container images MUST pin base image versions (no `latest` tags)
- **FR-005**: Container images MUST NOT contain hardcoded secrets or credentials
- **FR-006**: Docker Compose configuration MUST enable multi-container local testing with service dependencies defined
- **FR-006a**: Both frontend and backend applications MUST log to stdout/stderr (not to files). Logs MUST be accessible via `kubectl logs` command for debugging and monitoring.

#### Helm Chart Structure
- **FR-007**: Helm chart MUST follow standard structure with Chart.yaml, values.yaml, and templates/ directory
- **FR-008**: Frontend deployment template MUST support configurable replica count (default: 2)
- **FR-009**: Backend deployment template MUST support configurable replica count (default: 2)
- **FR-010**: Helm templates MUST include liveness and readiness probes for both frontend and backend
- **FR-011**: Helm values.yaml MUST parameterize image tags, replica counts, and resource limits
- **FR-012**: Helm chart MUST include ConfigMap for environment-specific configuration
- **FR-013**: Helm chart MUST include Secret management for sensitive data (database credentials, API keys)

#### Kubernetes Deployment
- **FR-014**: Minikube cluster MUST be initialized with minimum 4 CPU and 8GB RAM
- **FR-015**: Container images MUST be loadable into Minikube using `minikube image load` or Minikube Docker daemon
- **FR-016**: Application MUST be deployed using `helm install` or `helm upgrade` commands (no raw kubectl apply)
- **FR-017**: Frontend service MUST be accessible via NodePort or Minikube tunnel from host browser
- **FR-018**: Backend service MUST be accessible internally within cluster via ClusterIP service
- **FR-019**: Frontend pods MUST be able to discover and communicate with backend service via DNS
- **FR-019a**: Helm MUST retain last 3 revisions for rollback capability. If deployment fails health checks or verification, developer MUST use `helm rollback <release-name>` to restore previous working version. Deployment documentation MUST include rollback procedure.

#### Resource Management
- **FR-020**: All deployments MUST define resource requests and limits for CPU and memory. Frontend pods: 250m CPU request/limit, 512Mi memory request/limit. Backend pods: 200m CPU request/limit, 384Mi memory request/limit.
- **FR-021**: Deployments MUST specify minimum 2 replicas for both frontend and backend in production configuration

#### AI-Assisted Operations
- **FR-022**: Deployment process SHOULD utilize kubectl-ai for at least 3 Kubernetes operations
- **FR-023**: Docker operations MAY utilize Gordon (Docker AI Agent) if available, with fallback to standard Docker CLI
- **FR-024**: All AI tool interactions MUST be documented in an AI tools usage log

#### Documentation and Scripts
- **FR-025**: Deployment MUST include setup-minikube.sh script for Minikube initialization
- **FR-026**: Deployment MUST include build-images.sh script for Docker image builds
- **FR-027**: Deployment MUST include deploy.sh script for Helm deployment
- **FR-028**: Deployment MUST include teardown.sh script for cleanup operations
- **FR-029**: K8S-DEPLOYMENT.md MUST provide step-by-step deployment instructions enabling newcomers to deploy successfully

### Key Entities *(include if feature involves data)*

- **Container Image**: Immutable artifact containing application code, dependencies, and runtime configuration. Identified by repository name and tag (e.g., `todo-frontend:v1.0.0`). Related to Dockerfile, base image, and deployment manifests.

- **Helm Chart**: Package containing Kubernetes resource templates and configuration values. Contains Chart.yaml (metadata), values.yaml (configuration), and templates/ (resource definitions). Versioned independently from container images.

- **Pod**: Smallest deployable unit in Kubernetes, containing one or more containers. Has lifecycle (Pending, Running, Failed), resource allocations, and health check status. Managed by Deployment controller.

- **Service**: Abstraction providing stable network endpoint for accessing pods. Types include ClusterIP (internal), NodePort (external access via node port), and LoadBalancer. Provides DNS-based service discovery.

- **ConfigMap**: Key-value configuration data injected into pods as environment variables or files. Used for non-sensitive configuration like API endpoints, feature flags.

- **Secret**: Sensitive data (credentials, tokens) stored encrypted and injected into pods. Used for database passwords, API keys.

- **Deployment**: Controller managing pod replicas, rolling updates, and rollback. Ensures desired number of pod replicas are running.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developer can build both frontend and backend Docker images successfully in under 10 minutes total on standard development machine
- **SC-002**: Container images for frontend and backend are each under 500MB in size
- **SC-003**: Developer can deploy the application to Minikube using a single `helm install` command
- **SC-004**: All pods reach Running state within 2 minutes of Helm deployment
- **SC-005**: Application is accessible via browser and all Todo CRUD operations work end-to-end in Kubernetes environment
- **SC-006**: Frontend can communicate with backend API with response times under 1 second for typical operations
- **SC-007**: At least 2 replicas of frontend and 2 replicas of backend are running simultaneously
- **SC-008**: Health checks (liveness/readiness probes) are configured and functioning correctly
- **SC-009**: Developer can redeploy the application from scratch by following documentation in under 15 minutes
- **SC-010**: At least 3 kubectl-ai operations are successfully executed and documented
- **SC-011**: No secrets or credentials are hardcoded in container images or Kubernetes manifests
- **SC-012**: Deployment is reproducible from version-controlled code without manual intervention

### Quality Outcomes

- **SC-013**: Helm chart passes `helm lint` validation without errors
- **SC-014**: Dockerfiles follow container best practices (multi-stage builds, non-root user, pinned versions)
- **SC-015**: All deployment scripts are executable and include error handling
- **SC-016**: Documentation enables a developer unfamiliar with the project to deploy successfully on first attempt

## Assumptions

1. **Existing Application**: The Todo Chatbot application (Phase III) is complete and functional with working frontend and backend codebases
2. **Database Availability**: Database (likely Neon PostgreSQL) is accessible from Kubernetes pods (either external service or deployed separately)
3. **Local Development Environment**: Developer has a machine capable of running Minikube with 4 CPU and 8GB RAM minimum
4. **Base Image Availability**: Standard Node.js and Python base images are available from Docker Hub
5. **Network Connectivity**: Developer has internet access for pulling base images and installing tools
6. **Tool Availability**: Docker Desktop, Minikube, kubectl, and Helm are installed or can be installed by developer
7. **Authentication Mechanism**: Better Auth configuration from Phase III works in containerized environment with minimal changes
8. **Frontend Port**: Frontend application listens on port 3000 (standard Next.js default)
9. **Backend Port**: Backend application listens on a standard port (e.g., 8000 for FastAPI)
10. **AI Tools Optional**: kubectl-ai is preferred but Gordon is optional; deployment can succeed without Gordon if unavailable

## Constraints

### Technical Constraints
- MUST use Minikube for local Kubernetes (not cloud providers like EKS, GKE, AKS)
- MUST use Helm for deployment (raw Kubernetes manifests not acceptable)
- MUST support deployment on WSL 2 (Ubuntu-22.04) as per platform requirements
- Container images MUST be loadable into Minikube (registry considerations)
- SHOULD leverage AI tools where possible (kubectl-ai required, Gordon optional)

### Resource Constraints
- Minikube minimum: 4 CPU, 8GB RAM (documented in setup script)
- Container images target: under 500MB each
- Local disk space: sufficient for Minikube cluster, images, and build artifacts (~10GB recommended)

### Scope Constraints
- Deployment targets local development/testing only (production cloud deployment out of scope)
- Database deployment is NOT included (assumes external database or manual setup)
- CI/CD pipeline integration is out of scope
- Multi-cluster or multi-region deployment out of scope
- Advanced Kubernetes features (StatefulSets, DaemonSets, Operators) out of scope unless specifically needed

## Dependencies

### External Dependencies
- **Docker Desktop**: Required for building images and running containers locally
- **Minikube**: Required for local Kubernetes cluster
- **kubectl**: Required for Kubernetes cluster interaction
- **Helm 3.x**: Required for package management and deployment
- **kubectl-ai**: Recommended for AI-assisted operations
- **Gordon**: Optional for AI-assisted Docker operations
- **Neon PostgreSQL**: Database backend (assumed to be accessible externally or pre-configured)

### Internal Dependencies
- **Phase III Completion**: Todo Chatbot application must be fully functional (frontend + backend + database integration)
- **Better Auth Configuration**: Authentication setup from Phase III must be compatible with containerized environment
- **Environment Variables**: Existing .env configuration must be translatable to ConfigMaps/Secrets

### Assumptions About Dependencies
- Docker Desktop includes Kubernetes support but Minikube is used for consistency
- kubectl version is compatible with Minikube Kubernetes version
- Helm 3.x is used (Helm 2.x with Tiller is deprecated)
- kubectl-ai is installed globally or available in PATH

## Out of Scope

### Explicitly Excluded
- **Cloud Deployment**: AWS EKS, Google GKE, Azure AKS deployments
- **CI/CD Pipelines**: GitHub Actions, GitLab CI, Jenkins integration
- **Container Registry**: DockerHub, ECR, GCR, or private registry setup (images loaded directly to Minikube)
- **Database Containerization**: Deploying PostgreSQL within Kubernetes cluster
- **Monitoring and Observability**: Prometheus, Grafana, ELK stack integration
- **Service Mesh**: Istio, Linkerd integration
- **Advanced Networking**: Network policies, ingress controllers beyond basic Minikube ingress addon
- **Backup and Disaster Recovery**: Database backups, cluster backup strategies
- **Multi-Environment Deployment**: Automated promotion from dev to staging to production
- **Load Testing**: Performance testing under high load
- **Security Scanning**: Vulnerability scanning of container images (nice-to-have but not required)

### Future Considerations
- Production cloud deployment (Phase V potential)
- Automated CI/CD pipeline
- Infrastructure as Code with Terraform
- Advanced monitoring and alerting
- Multi-region high availability

## Clarified Decisions

### Database Connectivity Strategy
**Decision**: Keep Neon PostgreSQL external to the Kubernetes cluster.

**Rationale**: This approach maintains consistency with the production architecture, simplifies the Kubernetes setup by avoiding persistent volume configuration, and ensures the deployment matches real-world usage patterns. The backend pods will connect to the external Neon PostgreSQL service using connection strings provided via Kubernetes Secrets.

**Implementation Requirements**:
- Backend must have network connectivity from Minikube to external Neon service
- Database connection string stored in Kubernetes Secret
- ConfigMap includes non-sensitive database configuration (database name, connection pool settings)

### Better Auth Secrets Management
**Decision**: BETTER_AUTH_SECRET will be stored in a Kubernetes Secret created manually before Helm deployment.

**Rationale**: This provides the highest security by keeping secrets out of version control and Helm values files. It follows Kubernetes best practices for secret management and ensures secrets are encrypted at rest in etcd.

**Implementation Requirements**:
- Deployment documentation must include kubectl command to create the secret before `helm install`
- Example: `kubectl create secret generic auth-secrets --from-literal=BETTER_AUTH_SECRET=<value>`
- Helm chart references this pre-existing secret in deployment manifests
- Secret must be created in the same namespace as the application deployment

### Frontend-Backend Communication Configuration
**Decision**: Backend URL will be provided to the frontend via environment variable injected through ConfigMap.

**Rationale**: This approach maximizes portability and flexibility. The frontend can work in any environment (local development, Kubernetes, cloud) by simply changing the ConfigMap value. It follows the twelve-factor app methodology of storing configuration in the environment.

**Implementation Requirements**:
- ConfigMap defines `BACKEND_URL` (e.g., `http://backend-service:8000` for in-cluster communication)
- Frontend deployment injects this environment variable into Next.js containers
- Next.js application reads `process.env.BACKEND_URL` at runtime for API calls
- Different environments can use different ConfigMaps (dev, staging, prod) without code changes
