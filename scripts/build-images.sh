#!/bin/bash
set -e

# Build Docker images for Todo Chatbot
# This script builds both frontend and backend images and loads them into Minikube

echo "🏗️  Building Docker images for Todo Chatbot..."

# Ensure Docker is using Minikube daemon
echo "🐳 Configuring Docker environment to use Minikube..."
eval $(minikube docker-env)

# Build backend image
echo "📦 Building backend image (todo-backend:v1.0.0)..."
docker build -t todo-backend:v1.0.0 ./backend
if [ $? -eq 0 ]; then
    echo "✅ Backend image built successfully"
else
    echo "❌ Backend image build failed"
    exit 1
fi

# Build frontend image
echo "📦 Building frontend image (todo-frontend:v1.0.0)..."
docker build -t todo-frontend:v1.0.0 ./frontend
if [ $? -eq 0 ]; then
    echo "✅ Frontend image built successfully"
else
    echo "❌ Frontend image build failed"
    exit 1
fi

# Verify images are available in Minikube
echo "🔍 Verifying images in Minikube..."
echo ""
minikube image ls | grep todo

echo ""
echo "✅ Image build complete!"
echo ""
echo "📊 Image sizes:"
docker images | grep todo
echo ""
echo "📝 Next steps:"
echo "   1. Create secrets if not already created"
echo "   2. Deploy: ./scripts/deploy.sh"
echo ""
