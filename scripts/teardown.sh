#!/bin/bash

# Teardown Todo Chatbot Kubernetes deployment
# This script removes the Helm deployment and optionally stops Minikube

echo "🧹 Tearing down Todo Chatbot deployment..."

# Uninstall Helm release
if helm list | grep -q todo-chatbot; then
    echo "📦 Uninstalling Helm release..."
    helm uninstall todo-chatbot
    echo "✅ Helm release uninstalled"
else
    echo "⚠️  No Helm release found (todo-chatbot)"
fi

# Ask if user wants to stop Minikube
echo ""
read -p "Do you want to stop Minikube? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🛑 Stopping Minikube..."
    minikube stop
    echo "✅ Minikube stopped"
else
    echo "ℹ️  Minikube is still running"
fi

# Ask if user wants to delete Minikube cluster
echo ""
read -p "Do you want to delete the Minikube cluster completely? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Deleting Minikube cluster..."
    minikube delete
    echo "✅ Minikube cluster deleted"
else
    echo "ℹ️  Minikube cluster preserved"
fi

echo ""
echo "✅ Teardown complete!"
echo ""
