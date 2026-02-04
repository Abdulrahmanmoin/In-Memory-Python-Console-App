#!/bin/bash
set -e

# Deploy Todo Chatbot to Minikube using Helm
# This script checks for required secrets and deploys the application

echo "🚀 Deploying Todo Chatbot to Kubernetes..."

# Check if secrets exist
echo "🔐 Checking for required secrets..."

if ! kubectl get secret todo-backend-secrets &> /dev/null; then
    echo "⚠️  Warning: Secret 'todo-backend-secrets' not found!"
    echo ""
    echo "Please create the backend secrets first:"
    echo "  kubectl create secret generic todo-backend-secrets \\"
    echo "    --from-literal=OPENAI_API_KEY=sk-... \\"
    echo "    --from-literal=SECRET_KEY=your-secret-key \\"
    echo "    --from-literal=BETTER_AUTH_SECRET=your-auth-secret"
    echo ""
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

if ! kubectl get secret todo-database-secrets &> /dev/null; then
    echo "⚠️  Warning: Secret 'todo-database-secrets' not found!"
    echo ""
    echo "Please create the database secrets first:"
    echo "  kubectl create secret generic todo-database-secrets \\"
    echo "    --from-literal=DATABASE_URL=postgresql://..."
    echo ""
    read -p "Do you want to continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Determine environment (default to dev if not specified)
ENVIRONMENT=${1:-dev}
VALUES_FILE="./helm-charts/todo-chatbot/values-${ENVIRONMENT}.yaml"

if [ ! -f "$VALUES_FILE" ]; then
    echo "⚠️  Values file not found: $VALUES_FILE"
    echo "Using default values.yaml instead"
    VALUES_FILE="./helm-charts/todo-chatbot/values.yaml"
fi

echo "📦 Using values file: $VALUES_FILE"

# Deploy or upgrade with Helm
echo "📝 Deploying with Helm..."
helm upgrade --install todo-chatbot ./helm-charts/todo-chatbot \
    --values "$VALUES_FILE" \
    --wait \
    --timeout 5m

# Wait for pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=todo-chatbot --timeout=2m

# Display deployment status
echo ""
echo "📊 Deployment Status:"
kubectl get deployments
echo ""
kubectl get pods
echo ""
kubectl get services

# Get frontend URL
echo ""
echo "🌐 Getting frontend URL..."
FRONTEND_URL=$(minikube service todo-chatbot-frontend --url)

echo ""
echo "✅ Deployment complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend: $FRONTEND_URL"
echo ""
echo "📝 Useful commands:"
echo "   View logs: kubectl logs -l component=backend"
echo "   Scale: kubectl scale deployment/todo-chatbot-backend --replicas=3"
echo "   Delete: helm uninstall todo-chatbot"
echo ""
