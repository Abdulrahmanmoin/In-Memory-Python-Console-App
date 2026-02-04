# Quick Installation Guide

This guide provides step-by-step instructions for deploying the Todo Chatbot Helm chart.

## Prerequisites

1. **Kubernetes cluster** running (Minikube, Kind, or any K8s cluster)
2. **Helm 3.0+** installed
3. **kubectl** configured to access your cluster

## Step 1: Create Required Secrets

Before installing the chart, create the necessary secrets:

### Backend Secrets

```bash
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY="your-openai-api-key-here" \
  --from-literal=SECRET_KEY="your-random-secret-key-here"
```

### Database Secrets

```bash
kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL="postgresql://user:password@host:5432/database"
```

For development environment with different secret names:

```bash
kubectl create secret generic todo-backend-secrets-dev \
  --from-literal=OPENAI_API_KEY="your-dev-openai-key" \
  --from-literal=SECRET_KEY="dev-secret-key"

kubectl create secret generic todo-database-secrets-dev \
  --from-literal=DATABASE_URL="postgresql://user:password@localhost:5432/todo_dev"
```

For production environment:

```bash
kubectl create secret generic todo-backend-secrets-prod \
  --from-literal=OPENAI_API_KEY="your-prod-openai-key" \
  --from-literal=SECRET_KEY="prod-secret-key"

kubectl create secret generic todo-database-secrets-prod \
  --from-literal=DATABASE_URL="postgresql://user:password@prod-host:5432/todo_prod"
```

## Step 2: Validate the Chart

Run the validation script to ensure the chart is properly configured:

```bash
cd /mnt/d/todo_phase1
./helm-charts/todo-chatbot/validate-chart.sh
```

Note: Helm lint may fail in WSL environments due to path issues, but the chart structure is still valid.

## Step 3: Install the Chart

### Option A: Default Installation (2 replicas)

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot
```

### Option B: Development Installation (1 replica, reduced resources)

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-dev.yaml
```

### Option C: Production Installation (3 replicas, full resources)

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-prod.yaml
```

### Option D: Install in Specific Namespace

```bash
# Create namespace
kubectl create namespace todo-app

# Install in namespace
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -n todo-app \
  -f ./helm-charts/todo-chatbot/values-prod.yaml
```

### Option E: Dry Run (Preview without installing)

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --dry-run --debug
```

## Step 4: Verify Installation

Check the deployment status:

```bash
# View all resources
kubectl get all -l app.kubernetes.io/instance=todo-chatbot

# Check pods
kubectl get pods -l app=todo-chatbot

# Check services
kubectl get svc -l app=todo-chatbot

# View release status
helm status todo-chatbot

# View release notes
helm get notes todo-chatbot
```

## Step 5: Access the Application

### Get Node IP (for NodePort)

```bash
kubectl get nodes -o wide
```

Access the frontend at: `http://<NODE_IP>:30080`

### Alternative: Port Forwarding

```bash
# Forward frontend
kubectl port-forward svc/todo-chatbot-frontend 8080:80

# Access at http://localhost:8080
```

## Common Installation Scenarios

### Scenario 1: Local Development with Minikube

```bash
# Start Minikube
minikube start

# Create secrets
kubectl create secret generic todo-backend-secrets-dev \
  --from-literal=OPENAI_API_KEY="sk-..." \
  --from-literal=SECRET_KEY="dev-key"

kubectl create secret generic todo-database-secrets-dev \
  --from-literal=DATABASE_URL="postgresql://user:pass@localhost:5432/todo"

# Install chart
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-dev.yaml

# Get Minikube IP
minikube ip

# Access at http://<MINIKUBE_IP>:30080
```

### Scenario 2: Production Deployment

```bash
# Create production namespace
kubectl create namespace todo-prod

# Create secrets in production namespace
kubectl create secret generic todo-backend-secrets-prod \
  --from-literal=OPENAI_API_KEY="sk-prod-..." \
  --from-literal=SECRET_KEY="$(openssl rand -base64 32)" \
  -n todo-prod

kubectl create secret generic todo-database-secrets-prod \
  --from-literal=DATABASE_URL="postgresql://prod_user:secure_pass@prod-db:5432/todo_prod" \
  -n todo-prod

# Install with production values
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-prod.yaml \
  -n todo-prod

# Verify
kubectl get pods -n todo-prod
```

### Scenario 3: Custom Configuration

Create a custom values file `my-values.yaml`:

```yaml
backend:
  replicaCount: 4
  resources:
    requests:
      cpu: 500m
      memory: 1Gi

frontend:
  replicaCount: 4
  service:
    nodePort: 30090
```

Install with custom values:

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values.yaml \
  -f my-values.yaml
```

## Upgrading the Release

### Update Image Tags

```bash
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.image.tag=v1.1.0 \
  --set frontend.image.tag=v1.1.0
```

### Upgrade with New Values File

```bash
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  -f ./helm-charts/todo-chatbot/values-prod.yaml
```

### Reuse Existing Values

```bash
helm upgrade todo-chatbot ./helm-charts/todo-chatbot \
  --reuse-values \
  --set backend.replicaCount=5
```

## Rollback

```bash
# View release history
helm history todo-chatbot

# Rollback to previous version
helm rollback todo-chatbot

# Rollback to specific revision
helm rollback todo-chatbot 2
```

## Troubleshooting

### Pods not starting

```bash
# Check pod status
kubectl get pods -l app=todo-chatbot

# Describe pod
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>
```

### Secret errors

```bash
# Verify secrets exist
kubectl get secrets

# Check secret contents (base64 encoded)
kubectl get secret todo-backend-secrets -o yaml
```

### Service not accessible

```bash
# Check services
kubectl get svc -l app=todo-chatbot

# Test backend health
kubectl port-forward svc/todo-chatbot-backend 8000:8000
curl http://localhost:8000/health

# Test frontend health
kubectl port-forward svc/todo-chatbot-frontend 3000:80
curl http://localhost:3000/api/health
```

## Uninstalling

```bash
# Uninstall release
helm uninstall todo-chatbot

# Uninstall from specific namespace
helm uninstall todo-chatbot -n todo-prod

# Delete namespace (if desired)
kubectl delete namespace todo-prod

# Clean up secrets
kubectl delete secret todo-backend-secrets
kubectl delete secret todo-database-secrets
```

## Resource Requirements

### Development Environment

- **Backend**: 1 replica, 100m CPU, 256Mi RAM
- **Frontend**: 1 replica, 100m CPU, 256Mi RAM
- **Total**: ~200m CPU, ~512Mi RAM

### Default Environment

- **Backend**: 2 replicas, 200m CPU each, 384Mi RAM each
- **Frontend**: 2 replicas, 250m CPU each, 512Mi RAM each
- **Total**: ~900m CPU, ~1.8Gi RAM

### Production Environment

- **Backend**: 3 replicas, 200m CPU each, 384Mi RAM each
- **Frontend**: 3 replicas, 250m CPU each, 512Mi RAM each
- **Total**: ~1.35 CPU, ~2.7Gi RAM

Ensure your Kubernetes cluster has sufficient resources before deploying.

## Next Steps

After successful installation:

1. Monitor pod health: `kubectl get pods -w`
2. Check logs: `kubectl logs -l app=todo-chatbot --tail=100 -f`
3. Test health endpoints
4. Configure ingress (if needed)
5. Set up monitoring and alerting
6. Configure autoscaling (HPA) for production

For detailed configuration options, see the [README.md](README.md).
