# Kubernetes Frontend API URL Fix

## Problem

The frontend deployed in Minikube was calling `localhost` backend instead of the Minikube-deployed backend service. This was causing API calls to fail when accessing the frontend through `minikube service todo-chatbot-frontend`.

## Root Cause

Next.js `NEXT_PUBLIC_*` environment variables are embedded into the JavaScript bundle at **build time**, not runtime. The frontend Docker image was built with the default value, which pointed to `localhost:7860`.

Even though we updated the Kubernetes ConfigMap with the correct backend URL, the change had no effect because:
1. Next.js bakes `NEXT_PUBLIC_*` variables during the build process
2. These variables cannot be changed after the image is built

## Solution

### 1. Updated Dockerfile to Accept Build Argument

Modified `frontend/Dockerfile` to accept a build-time argument for the API URL:

```dockerfile
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}
```

### 2. Updated Helm Chart Configuration

Updated the Helm chart to support runtime API URL configuration:

**ConfigMap** (`helm-charts/todo-chatbot/templates/configmap.yaml`):
```yaml
data:
  NEXT_PUBLIC_API_URL: "http://{{ backend-service-name }}:{{ port }}"
```

**Frontend Deployment** (`helm-charts/todo-chatbot/templates/frontend-deployment.yaml`):
```yaml
env:
  - name: NEXT_PUBLIC_API_URL
    valueFrom:
      configMapKeyRef:
        name: todo-chatbot-config
        key: NEXT_PUBLIC_API_URL
```

### 3. Rebuilt Frontend Image with Correct API URL

Rebuilt the frontend Docker image with the Minikube backend NodePort URL:

```bash
eval $(minikube docker-env)
docker build -t todo-frontend:v1.0.2 \
  --build-arg NEXT_PUBLIC_API_URL="http://127.0.0.1:30827" \
  ./frontend
```

### 4. Restarted Frontend Pods

```bash
kubectl delete pod -l component=frontend
```

## Service URLs

- **Frontend**: `http://127.0.0.1:32909` (minikube service todo-chatbot-frontend)
- **Backend**: `http://127.0.0.1:30827` (minikube service todo-chatbot-backend)

## Testing

After applying the fix, you can test by:

1. Access the frontend: `minikube service todo-chatbot-frontend`
2. Open browser developer tools (F12) and go to Network tab
3. Try to login or create a task
4. Verify that API calls are going to `http://127.0.0.1:30827` (not localhost:7860)

## Important Notes

### For Production Deployments

In production with proper Ingress controller, you would:
1. Set up an Ingress for both frontend and backend
2. Use a public domain name (e.g., `https://api.example.com`)
3. Build the frontend image with that production URL:
   ```bash
   docker build -t frontend:prod \
     --build-arg NEXT_PUBLIC_API_URL="https://api.example.com" \
     ./frontend
   ```

### For Local Development

For local development outside Kubernetes:
1. Use the default `.env` file with `NEXT_PUBLIC_API_URL=http://localhost:8000`
2. Run both backend and frontend locally

### Alternative: Runtime Configuration

For more flexibility, consider implementing a runtime configuration approach:
1. Create a Next.js API route that returns configuration
2. Fetch the config on app initialization
3. Use that config throughout the app

This allows changing the API URL without rebuilding the image, but requires code changes.

## Files Modified

1. `frontend/Dockerfile` - Added ARG for NEXT_PUBLIC_API_URL
2. `helm-charts/todo-chatbot/templates/configmap.yaml` - Updated to use NEXT_PUBLIC_API_URL
3. `helm-charts/todo-chatbot/templates/frontend-deployment.yaml` - Updated env var name
4. `helm-charts/todo-chatbot/values.yaml` - Added API URL override option

## Related Documentation

- [Next.js Environment Variables](https://nextjs.org/docs/pages/building-your-application/configuring/environment-variables)
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Docker Build Arguments](https://docs.docker.com/engine/reference/builder/#arg)
