# Todo Chatbot Helm Chart

A production-ready Helm chart for deploying the Todo Chatbot application on Kubernetes. This chart deploys a full-stack application with a FastAPI backend and Next.js frontend.

## Overview

This chart provides a complete deployment of:
- **Backend**: FastAPI-based REST API with Python 3.11
- **Frontend**: Next.js application with React
- **Configuration**: Environment-specific ConfigMaps
- **Secrets**: External secret management (secrets created manually)

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- kubectl configured to communicate with your cluster
- Pre-created Kubernetes secrets (see Secrets section below)

## Chart Details

**Chart Version**: 1.0.0
**App Version**: 1.0.0

## Quick Start

### 1. Create Required Secrets

Before installing the chart, create the required secrets:

```bash
# Backend secrets
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=your-openai-api-key \
  --from-literal=SECRET_KEY=your-secret-key

# Database secrets
kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### 2. Install the Chart

```bash
# Default installation (production values)
helm install todo-chatbot ./helm-charts/todo-chatbot

# Development installation
helm install todo-chatbot ./helm-charts/todo-chatbot -f ./helm-charts/todo-chatbot/values-dev.yaml

# Production installation
helm install todo-chatbot ./helm-charts/todo-chatbot -f ./helm-charts/todo-chatbot/values-prod.yaml

# Install in specific namespace
helm install todo-chatbot ./helm-charts/todo-chatbot -n todo-app --create-namespace
```

### 3. Verify Installation

```bash
# Check pod status
kubectl get pods -l app.kubernetes.io/instance=todo-chatbot

# View release information
helm status todo-chatbot

# Access application (NodePort)
kubectl get nodes -o wide  # Get node IP
# Then visit http://<NODE_IP>:30080
```

## Configuration

### Values Files

The chart includes three values files for different environments:

- **values.yaml**: Default production configuration (2 replicas each)
- **values-dev.yaml**: Development configuration (1 replica, reduced resources)
- **values-prod.yaml**: Production configuration (3 replicas, full resources)

### Key Configuration Parameters

#### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend replicas | `2` |
| `backend.image.repository` | Backend image repository | `todo-backend` |
| `backend.image.tag` | Backend image tag | `v1.0.0` |
| `backend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `backend.service.type` | Kubernetes service type | `ClusterIP` |
| `backend.service.port` | Service port | `8000` |
| `backend.resources.requests.cpu` | CPU request | `200m` |
| `backend.resources.requests.memory` | Memory request | `384Mi` |
| `backend.resources.limits.cpu` | CPU limit | `200m` |
| `backend.resources.limits.memory` | Memory limit | `384Mi` |

#### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend replicas | `2` |
| `frontend.image.repository` | Frontend image repository | `todo-frontend` |
| `frontend.image.tag` | Frontend image tag | `v1.0.0` |
| `frontend.image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `frontend.service.type` | Kubernetes service type | `NodePort` |
| `frontend.service.port` | Service port | `80` |
| `frontend.service.nodePort` | NodePort for external access | `30080` |
| `frontend.resources.requests.cpu` | CPU request | `250m` |
| `frontend.resources.requests.memory` | Memory request | `512Mi` |
| `frontend.resources.limits.cpu` | CPU limit | `250m` |
| `frontend.resources.limits.memory` | Memory limit | `512Mi` |

#### ConfigMap Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `configMap.NODE_ENV` | Node environment | `production` |
| `configMap.LOG_LEVEL` | Application log level | `info` |

#### Secret References

| Parameter | Description | Default |
|-----------|-------------|---------|
| `secrets.backendSecretName` | Name of backend secrets | `todo-backend-secrets` |
| `secrets.databaseSecretName` | Name of database secrets | `todo-database-secrets` |

### Overriding Values

You can override any value using `--set`:

```bash
# Override replica count
helm install todo-chatbot ./helm-charts/todo-chatbot --set backend.replicaCount=5

# Override image tag
helm install todo-chatbot ./helm-charts/todo-chatbot --set frontend.image.tag=v2.0.0

# Override multiple values
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.replicaCount=3 \
  --set frontend.replicaCount=3 \
  --set configMap.LOG_LEVEL=debug
```

Or create a custom values file:

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot -f custom-values.yaml
```

## Secrets Management

This chart requires two secrets to be created manually before deployment:

### Backend Secrets (`todo-backend-secrets`)

Required keys:
- `OPENAI_API_KEY`: OpenAI API key for AI functionality
- `SECRET_KEY`: Application secret key for security

```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=sk-... \
  --from-literal=SECRET_KEY=your-random-secret-key
```

### Database Secrets (`todo-database-secrets`)

Required keys:
- `DATABASE_URL`: PostgreSQL connection string

```bash
kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=postgresql://user:pass@host:5432/db
```

For production, consider using external secret management solutions:
- [External Secrets Operator](https://external-secrets.io/)
- [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets)
- Cloud provider secret managers (AWS Secrets Manager, GCP Secret Manager, Azure Key Vault)

## Health Checks

The chart includes health probes for both services:

### Backend
- **Liveness Probe**: `GET /health` (initial delay: 30s, period: 10s)
- **Readiness Probe**: `GET /health` (initial delay: 10s, period: 5s)

### Frontend
- **Liveness Probe**: `GET /api/health` (initial delay: 30s, period: 10s)
- **Readiness Probe**: `GET /api/health` (initial delay: 10s, period: 5s)

## Accessing the Application

### NodePort (Default)

Get the node IP and access via NodePort:

```bash
kubectl get nodes -o wide
# Access at http://<NODE_IP>:30080
```

### Port Forwarding

Forward the frontend service to localhost:

```bash
kubectl port-forward svc/todo-chatbot-frontend 8080:80
# Access at http://localhost:8080
```

### Backend API Access

The backend is only accessible within the cluster by default. For local testing:

```bash
kubectl port-forward svc/todo-chatbot-backend 8000:8000
# Access at http://localhost:8000
```

## Upgrading

```bash
# Upgrade with default values
helm upgrade todo-chatbot ./helm-charts/todo-chatbot

# Upgrade with specific values file
helm upgrade todo-chatbot ./helm-charts/todo-chatbot -f values-prod.yaml

# Upgrade with value overrides
helm upgrade todo-chatbot ./helm-charts/todo-chatbot --set backend.image.tag=v1.1.0
```

## Rollback

```bash
# Rollback to previous release
helm rollback todo-chatbot

# Rollback to specific revision
helm rollback todo-chatbot 2

# View release history
helm history todo-chatbot
```

## Uninstalling

```bash
# Uninstall the release
helm uninstall todo-chatbot

# Uninstall and keep history
helm uninstall todo-chatbot --keep-history
```

## Validation

Before deploying, validate the chart:

```bash
# Lint the chart
helm lint ./helm-charts/todo-chatbot

# Dry run installation
helm install todo-chatbot ./helm-charts/todo-chatbot --dry-run --debug

# Template rendering (preview manifests)
helm template todo-chatbot ./helm-charts/todo-chatbot

# Template with specific values
helm template todo-chatbot ./helm-charts/todo-chatbot -f values-dev.yaml
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -l app.kubernetes.io/instance=todo-chatbot
kubectl describe pod <pod-name>
```

### View Logs

```bash
# Backend logs
kubectl logs -l component=backend --tail=100 -f

# Frontend logs
kubectl logs -l component=frontend --tail=100 -f
```

### Check Services

```bash
kubectl get svc -l app.kubernetes.io/instance=todo-chatbot
```

### Check ConfigMap

```bash
kubectl get configmap todo-chatbot-config -o yaml
```

### Common Issues

**Pods not starting:**
- Check if required secrets exist: `kubectl get secrets`
- Verify secret keys match expected names
- Check image pull policy and image availability

**Probes failing:**
- Verify health endpoints are accessible
- Check if initialDelaySeconds is sufficient for app startup
- Review pod logs for application errors

**Cannot access application:**
- Verify NodePort service: `kubectl get svc`
- Check firewall rules allow NodePort traffic
- Confirm node IP is accessible from your location

## Environment-Specific Deployments

### Development

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f values-dev.yaml \
  -n todo-dev \
  --create-namespace
```

**Development characteristics:**
- 1 replica per service
- Reduced resources (100m CPU, 256Mi RAM)
- Debug logging
- Always pull images

### Production

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f values-prod.yaml \
  -n todo-prod \
  --create-namespace
```

**Production characteristics:**
- 3 replicas per service (high availability)
- Full resources (200m/250m CPU, 384Mi/512Mi RAM)
- Info-level logging
- IfNotPresent pull policy

## Chart Structure

```
helm-charts/todo-chatbot/
├── Chart.yaml                          # Chart metadata
├── values.yaml                         # Default values
├── values-dev.yaml                     # Development values
├── values-prod.yaml                    # Production values
├── .helmignore                         # Files to ignore
├── README.md                           # This file
└── templates/
    ├── _helpers.tpl                    # Template helpers
    ├── backend-deployment.yaml         # Backend Deployment
    ├── backend-service.yaml            # Backend Service
    ├── frontend-deployment.yaml        # Frontend Deployment
    ├── frontend-service.yaml           # Frontend Service
    ├── configmap.yaml                  # ConfigMap
    └── NOTES.txt                       # Post-install notes
```

## Best Practices

1. **Secrets**: Always create secrets before deploying the chart
2. **Resource Limits**: Set appropriate resource limits for your environment
3. **Health Checks**: Monitor probe metrics to tune initialDelaySeconds
4. **Image Tags**: Use specific version tags, avoid `latest` in production
5. **Namespaces**: Deploy to dedicated namespaces per environment
6. **Values Files**: Maintain separate values files for each environment
7. **Version Control**: Track custom values files in version control
8. **Testing**: Always test with `--dry-run` before actual deployment

## Contributing

When modifying this chart:
1. Update version in `Chart.yaml` following semantic versioning
2. Test with `helm lint`
3. Validate with `helm template`
4. Test deployment with `--dry-run`
5. Update this README with any new parameters

## License

This chart is part of the Todo Chatbot project.

## Support

For issues or questions:
- GitHub Issues: https://github.com/your-org/todo-chatbot/issues
- Documentation: https://github.com/your-org/todo-chatbot
