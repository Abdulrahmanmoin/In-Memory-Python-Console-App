# Helm Chart Configuration Reference

This document provides a comprehensive reference for all configuration options in the Todo Chatbot Helm chart.

## Chart Metadata

Defined in `Chart.yaml`:

```yaml
apiVersion: v2
name: todo-chatbot
version: 1.0.0
appVersion: "1.0.0"
type: application
```

## Environment Comparison

| Configuration | Development | Default | Production |
|--------------|-------------|---------|------------|
| **Backend Replicas** | 1 | 2 | 3 |
| **Frontend Replicas** | 1 | 2 | 3 |
| **Backend CPU** | 100m | 200m | 200m |
| **Backend Memory** | 256Mi | 384Mi | 384Mi |
| **Frontend CPU** | 100m | 250m | 250m |
| **Frontend Memory** | 256Mi | 512Mi | 512Mi |
| **Image Pull Policy** | Always | IfNotPresent | IfNotPresent |
| **NODE_ENV** | development | production | production |
| **LOG_LEVEL** | debug | info | info |
| **Total CPU** | ~200m | ~900m | ~1350m |
| **Total Memory** | ~512Mi | ~1.8Gi | ~2.7Gi |

## Values Structure

### Backend Configuration

```yaml
backend:
  replicaCount: 2                        # Number of backend pods

  image:
    repository: todo-backend             # Docker image repository
    tag: "v1.0.0"                       # Image tag
    pullPolicy: IfNotPresent            # When to pull images

  service:
    type: ClusterIP                     # Internal-only service
    port: 8000                          # Service port
    targetPort: 8000                    # Container port

  resources:
    requests:
      cpu: 200m                         # Guaranteed CPU
      memory: 384Mi                     # Guaranteed memory
    limits:
      cpu: 200m                         # Maximum CPU
      memory: 384Mi                     # Maximum memory

  livenessProbe:
    httpGet:
      path: /health                     # Health check endpoint
      port: 8000
    initialDelaySeconds: 30             # Wait before first check
    periodSeconds: 10                   # Check interval
    timeoutSeconds: 5                   # Request timeout
    failureThreshold: 3                 # Failures before restart

  readinessProbe:
    httpGet:
      path: /health
      port: 8000
    initialDelaySeconds: 10
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
```

### Frontend Configuration

```yaml
frontend:
  replicaCount: 2                        # Number of frontend pods

  image:
    repository: todo-frontend            # Docker image repository
    tag: "v1.0.0"                       # Image tag
    pullPolicy: IfNotPresent            # When to pull images

  service:
    type: NodePort                      # External access via NodePort
    port: 80                            # Service port
    targetPort: 3000                    # Container port
    nodePort: 30080                     # External port on nodes

  resources:
    requests:
      cpu: 250m                         # Guaranteed CPU
      memory: 512Mi                     # Guaranteed memory
    limits:
      cpu: 250m                         # Maximum CPU
      memory: 512Mi                     # Maximum memory

  livenessProbe:
    httpGet:
      path: /api/health                 # Health check endpoint
      port: 3000
    initialDelaySeconds: 30             # Wait before first check
    periodSeconds: 10                   # Check interval
    timeoutSeconds: 5                   # Request timeout
    failureThreshold: 3                 # Failures before restart

  readinessProbe:
    httpGet:
      path: /api/health
      port: 3000
    initialDelaySeconds: 10
    periodSeconds: 5
    timeoutSeconds: 3
    failureThreshold: 3
```

### ConfigMap Settings

```yaml
configMap:
  BACKEND_URL: ""                       # Auto-generated from service name
  NODE_ENV: "production"                # Node environment
  LOG_LEVEL: "info"                     # Application log level
```

The `BACKEND_URL` is automatically constructed as:
```
http://{{ release-name }}-backend:8000
```

### Secret References

```yaml
secrets:
  backendSecretName: "todo-backend-secrets"      # Backend secret name
  databaseSecretName: "todo-database-secrets"    # Database secret name
```

## Environment Variables

### Backend Container

Environment variables injected into backend pods:

| Variable | Source | Description |
|----------|--------|-------------|
| `BACKEND_URL` | ConfigMap | Internal backend service URL |
| `LOG_LEVEL` | ConfigMap | Logging verbosity |
| `DATABASE_URL` | Secret (database) | PostgreSQL connection string |
| `OPENAI_API_KEY` | Secret (backend) | OpenAI API key |
| `SECRET_KEY` | Secret (backend) | Application secret key |

### Frontend Container

Environment variables injected into frontend pods:

| Variable | Source | Description |
|----------|--------|-------------|
| `BACKEND_URL` | ConfigMap | Backend API URL for frontend |
| `NODE_ENV` | ConfigMap | Node environment (production/development) |
| `LOG_LEVEL` | ConfigMap | Logging verbosity |

## Health Probes

### Liveness Probes

Determines if a pod needs to be restarted:

- **Backend**: `GET /health` on port 8000
  - Initial delay: 30s (allow app startup)
  - Check every: 10s
  - Timeout: 5s
  - Restart after: 3 failures

- **Frontend**: `GET /api/health` on port 3000
  - Initial delay: 30s (allow app startup)
  - Check every: 10s
  - Timeout: 5s
  - Restart after: 3 failures

### Readiness Probes

Determines if a pod can receive traffic:

- **Backend**: `GET /health` on port 8000
  - Initial delay: 10s
  - Check every: 5s
  - Timeout: 3s
  - Mark unready after: 3 failures

- **Frontend**: `GET /api/health` on port 3000
  - Initial delay: 10s
  - Check every: 5s
  - Timeout: 3s
  - Mark unready after: 3 failures

## Labels and Selectors

### Common Labels (All Resources)

Applied to all resources via `_helpers.tpl`:

```yaml
labels:
  helm.sh/chart: todo-chatbot-1.0.0
  app.kubernetes.io/name: todo-chatbot
  app.kubernetes.io/instance: {{ .Release.Name }}
  app.kubernetes.io/version: "1.0.0"
  app.kubernetes.io/managed-by: Helm
```

### Backend Labels

Additional labels for backend resources:

```yaml
app: todo-chatbot
component: backend
```

### Frontend Labels

Additional labels for frontend resources:

```yaml
app: todo-chatbot
component: frontend
```

## Service Configuration

### Backend Service

- **Type**: ClusterIP (internal only)
- **Port**: 8000 (service port)
- **TargetPort**: 8000 (container port)
- **Access**: Only accessible within cluster
- **DNS**: `{{ release-name }}-backend.{{ namespace }}.svc.cluster.local`

### Frontend Service

- **Type**: NodePort (external access)
- **Port**: 80 (service port)
- **TargetPort**: 3000 (container port)
- **NodePort**: 30080 (external port on all nodes)
- **Access**: External via `http://<NODE_IP>:30080`
- **DNS**: `{{ release-name }}-frontend.{{ namespace }}.svc.cluster.local`

## Resource Quotas

### Minimum Cluster Requirements

To run this chart, your cluster needs:

**Development Environment:**
- Nodes: 1
- Total CPU: 200m (0.2 cores)
- Total Memory: 512Mi

**Default Environment:**
- Nodes: 1-2
- Total CPU: 900m (0.9 cores)
- Total Memory: 1.8Gi

**Production Environment:**
- Nodes: 2-3 (for pod distribution)
- Total CPU: 1350m (1.35 cores)
- Total Memory: 2.7Gi

### Pod Distribution

With multiple replicas, pods are distributed based on Kubernetes default scheduling:

- Prefers spreading across nodes (when multiple nodes available)
- Considers resource availability
- Respects node taints and tolerations (if configured)

## Customization Examples

### Change Number of Replicas

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.replicaCount=5 \
  --set frontend.replicaCount=5
```

### Use Different Image Tags

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.image.tag=v2.0.0 \
  --set frontend.image.tag=v2.0.0
```

### Adjust Resource Limits

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set backend.resources.limits.cpu=500m \
  --set backend.resources.limits.memory=1Gi
```

### Change NodePort

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set frontend.service.nodePort=30090
```

### Custom Secret Names

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set secrets.backendSecretName=my-backend-secrets \
  --set secrets.databaseSecretName=my-db-secrets
```

### Enable Debug Logging

```bash
helm install todo-chatbot ./helm-charts/todo-chatbot \
  --set configMap.LOG_LEVEL=debug \
  --set configMap.NODE_ENV=development
```

## Template Helpers

Defined in `templates/_helpers.tpl`:

| Helper | Purpose | Example Output |
|--------|---------|----------------|
| `todo-chatbot.name` | Chart name | `todo-chatbot` |
| `todo-chatbot.fullname` | Full resource name | `my-release-todo-chatbot` |
| `todo-chatbot.chart` | Chart version label | `todo-chatbot-1.0.0` |
| `todo-chatbot.labels` | Common labels | (See Labels section) |
| `todo-chatbot.selectorLabels` | Selector labels | `app.kubernetes.io/name`, `app.kubernetes.io/instance` |
| `todo-chatbot.backend.labels` | Backend labels | Common + component=backend |
| `todo-chatbot.backend.selectorLabels` | Backend selectors | Selectors + component=backend |
| `todo-chatbot.frontend.labels` | Frontend labels | Common + component=frontend |
| `todo-chatbot.frontend.selectorLabels` | Frontend selectors | Selectors + component=frontend |
| `todo-chatbot.backend.serviceName` | Backend service | `my-release-backend` |
| `todo-chatbot.frontend.serviceName` | Frontend service | `my-release-frontend` |
| `todo-chatbot.configMapName` | ConfigMap name | `my-release-config` |

## Security Considerations

### Secrets Management

This chart does NOT create secrets automatically. You must create them manually:

```bash
# Required secrets
kubectl create secret generic todo-backend-secrets \
  --from-literal=OPENAI_API_KEY=... \
  --from-literal=SECRET_KEY=...

kubectl create secret generic todo-database-secrets \
  --from-literal=DATABASE_URL=...
```

### Best Practices

1. **Use External Secret Managers**: Consider External Secrets Operator, Sealed Secrets, or cloud provider solutions
2. **Rotate Secrets Regularly**: Update secrets periodically
3. **Use RBAC**: Limit access to secrets
4. **Encrypt at Rest**: Enable Kubernetes secret encryption
5. **Least Privilege**: Grant minimal permissions needed

### Image Security

- **Image Pull Policy**: `IfNotPresent` in production to use verified images
- **Image Tags**: Always use specific version tags, never `latest`
- **Private Registry**: Use `imagePullSecrets` for private registries

## Networking

### Service Mesh Integration

This chart is compatible with service meshes (Istio, Linkerd):

- Services use standard Kubernetes networking
- No special annotations required
- Can add sidecar injection via namespace labels

### Ingress Configuration

To add Ingress (not included by default):

```yaml
# custom-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-chatbot-ingress
spec:
  rules:
  - host: todo.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {{ release-name }}-frontend
            port:
              number: 80
```

## Scaling

### Manual Scaling

```bash
kubectl scale deployment/{{ release-name }}-backend --replicas=5
kubectl scale deployment/{{ release-name }}-frontend --replicas=5
```

### Horizontal Pod Autoscaler (HPA)

Create HPA for automatic scaling:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-chatbot-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ release-name }}-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring

### Prometheus Integration

Add annotations for Prometheus scraping:

```yaml
# Add to deployment metadata.annotations
prometheus.io/scrape: "true"
prometheus.io/port: "8000"
prometheus.io/path: "/metrics"
```

### Log Aggregation

Logs are written to stdout/stderr and can be collected by:

- Fluentd
- Fluent Bit
- Loki
- CloudWatch (EKS)
- Stackdriver (GKE)

Access logs:
```bash
kubectl logs -l component=backend --tail=100 -f
kubectl logs -l component=frontend --tail=100 -f
```

## Troubleshooting Configuration

### Common Issues

1. **Pods CrashLoopBackOff**: Check secret names match exactly
2. **ImagePullBackOff**: Verify image names and tags exist
3. **Readiness probe fails**: Increase `initialDelaySeconds` if app starts slowly
4. **Out of memory**: Increase `resources.limits.memory`
5. **CPU throttling**: Increase `resources.limits.cpu`

### Debug Commands

```bash
# View effective values
helm get values todo-chatbot

# View all rendered manifests
helm get manifest todo-chatbot

# Describe pod for events
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name> --previous  # Previous container if crashed
```

## Advanced Configuration

### Node Affinity

Add to values.yaml to schedule on specific nodes:

```yaml
backend:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: node-type
            operator: In
            values:
            - backend
```

### Pod Anti-Affinity

Spread pods across nodes:

```yaml
backend:
  affinity:
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: component
              operator: In
              values:
              - backend
          topologyKey: kubernetes.io/hostname
```

### Tolerations

Allow pods on tainted nodes:

```yaml
backend:
  tolerations:
  - key: "dedicated"
    operator: "Equal"
    value: "backend"
    effect: "NoSchedule"
```

## Version Upgrade Path

When upgrading chart versions:

1. Review CHANGELOG for breaking changes
2. Backup current values: `helm get values todo-chatbot > backup-values.yaml`
3. Test in dev environment first
4. Use `--dry-run` to preview changes
5. Upgrade with backup plan: `helm upgrade --atomic todo-chatbot ./helm-charts/todo-chatbot`
6. Monitor pod health after upgrade
7. Rollback if needed: `helm rollback todo-chatbot`

## Support Matrix

| Component | Minimum Version | Recommended Version |
|-----------|----------------|---------------------|
| Kubernetes | 1.19+ | 1.25+ |
| Helm | 3.0+ | 3.10+ |
| Docker | 19.03+ | 20.10+ |

## References

- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Best Practices Guide](https://helm.sh/docs/chart_best_practices/)
- Chart README: [README.md](README.md)
- Installation Guide: [INSTALL.md](INSTALL.md)
