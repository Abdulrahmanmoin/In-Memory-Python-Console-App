#!/bin/bash
set -e

# Setup Minikube for Todo Chatbot K8s Deployment
# This script initializes a Minikube cluster with required resources and addons

echo "🚀 Setting up Minikube cluster..."

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo "❌ Error: Minikube is not installed. Please install it first."
    echo "Visit: https://minikube.sigs.k8s.io/docs/start/"
    exit 1
fi

# Check if Minikube is already running
if minikube status | grep -q "Running"; then
    echo "⚠️  Minikube is already running. Stopping existing cluster..."
    minikube stop
fi

# Start Minikube with required resources
echo "📦 Starting Minikube with 4 CPU and 8GB RAM..."
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable required addons
echo "🔌 Enabling Minikube addons..."
minikube addons enable ingress
minikube addons enable metrics-server

# Configure Docker environment to use Minikube daemon
echo "🐳 Configuring Docker environment..."
eval $(minikube docker-env)

# Verify cluster is running
echo "✅ Verifying cluster status..."
kubectl cluster-info
kubectl get nodes

echo ""
echo "✅ Minikube setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Run: eval \$(minikube docker-env)"
echo "   2. Build images: ./scripts/build-images.sh"
echo "   3. Create secrets: kubectl create secret generic ..."
echo "   4. Deploy: ./scripts/deploy.sh"
echo ""
