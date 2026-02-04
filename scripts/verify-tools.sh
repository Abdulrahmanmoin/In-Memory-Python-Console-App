#!/bin/bash
# Verification script for Docker, Minikube, Helm, and kubectl
# Run this to check if all tools are installed and working correctly

set -e

echo "=================================="
echo "Tool Verification Script"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print warning
warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check Docker
echo "1. Checking Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>&1)
    success "Docker installed: $DOCKER_VERSION"

    if docker ps &> /dev/null; then
        success "Docker daemon is running"
        RUNNING_CONTAINERS=$(docker ps --format "{{.Names}}" | wc -l)
        echo "   Running containers: $RUNNING_CONTAINERS"
    else
        error "Docker daemon is not running or not accessible"
        echo "   Solution: Enable Docker Desktop WSL integration"
        echo "   Settings → Resources → WSL Integration → Enable your distro"
    fi
else
    error "Docker is not installed or not in PATH"
fi
echo ""

# Check Minikube
echo "2. Checking Minikube..."
if command -v minikube &> /dev/null; then
    MINIKUBE_VERSION=$(minikube version --short 2>&1)
    success "Minikube installed: $MINIKUBE_VERSION"

    MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>&1 || echo "Stopped")
    if [ "$MINIKUBE_STATUS" = "Running" ]; then
        success "Minikube is running"

        # Get cluster info
        MINIKUBE_IP=$(minikube ip 2>&1 || echo "N/A")
        MINIKUBE_PROFILE=$(minikube profile 2>&1 || echo "N/A")
        K8S_VERSION=$(minikube kubectl -- version --short 2>&1 | grep Server | awk '{print $3}' || echo "N/A")

        echo "   Profile: $MINIKUBE_PROFILE"
        echo "   Cluster IP: $MINIKUBE_IP"
        echo "   Kubernetes: $K8S_VERSION"

        # Check addons
        echo "   Checking addons..."
        INGRESS_STATUS=$(minikube addons list | grep ingress | awk '{print $3}' || echo "unknown")
        METRICS_STATUS=$(minikube addons list | grep metrics-server | awk '{print $3}' || echo "unknown")

        if [ "$INGRESS_STATUS" = "enabled" ]; then
            success "   Ingress addon: enabled"
        else
            warning "   Ingress addon: disabled"
        fi

        if [ "$METRICS_STATUS" = "enabled" ]; then
            success "   Metrics-server addon: enabled"
        else
            warning "   Metrics-server addon: disabled"
        fi
    else
        warning "Minikube is not running (Status: $MINIKUBE_STATUS)"
        echo "   To start: minikube start --cpus=4 --memory=3500 --driver=docker"
    fi
else
    error "Minikube is not installed or not in PATH"
fi
echo ""

# Check kubectl
echo "3. Checking kubectl..."
if command -v kubectl &> /dev/null; then
    KUBECTL_VERSION=$(kubectl version --client --short 2>&1 | grep -oP 'v[\d.]+' || echo "unknown")
    success "kubectl installed: $KUBECTL_VERSION"

    if kubectl cluster-info &> /dev/null; then
        success "kubectl can connect to cluster"
        CURRENT_CONTEXT=$(kubectl config current-context 2>&1 || echo "none")
        echo "   Current context: $CURRENT_CONTEXT"

        # Check nodes
        NODE_STATUS=$(kubectl get nodes --no-headers 2>&1 | awk '{print $2}' || echo "Error")
        if [ "$NODE_STATUS" = "Ready" ]; then
            success "   Node status: Ready"
        else
            warning "   Node status: $NODE_STATUS"
        fi

        # Check namespaces
        NAMESPACE_COUNT=$(kubectl get namespaces --no-headers 2>&1 | wc -l || echo "0")
        echo "   Namespaces: $NAMESPACE_COUNT"
    else
        warning "kubectl cannot connect to cluster"
        echo "   Make sure Minikube is running"
    fi
else
    error "kubectl is not installed or not in PATH"
fi
echo ""

# Check Helm
echo "4. Checking Helm..."
if command -v helm &> /dev/null; then
    HELM_VERSION=$(helm version --short 2>&1)
    success "Helm installed: $HELM_VERSION"

    if helm list &> /dev/null; then
        success "Helm can connect to cluster"
        RELEASES=$(helm list --short 2>&1 || echo "")
        if [ -z "$RELEASES" ]; then
            echo "   No Helm releases deployed"
        else
            echo "   Deployed releases:"
            helm list --short | while read release; do
                echo "     - $release"
            done
        fi
    else
        warning "Helm cannot connect to cluster"
    fi
else
    error "Helm is not installed or not in PATH"
fi
echo ""

# Check kubectl-ai
echo "5. Checking kubectl-ai (optional)..."
if command -v kubectl-ai &> /dev/null; then
    success "kubectl-ai is installed"
    KUBECTL_AI_PATH=$(which kubectl-ai)
    echo "   Path: $KUBECTL_AI_PATH"
else
    warning "kubectl-ai is not installed (optional tool)"
fi
echo ""

# Check Gordon (Docker AI)
echo "6. Checking Gordon/Docker AI (optional)..."
if docker ai --help &> /dev/null 2>&1; then
    success "Gordon (Docker AI) is available"
else
    warning "Gordon (Docker AI) is not available (optional tool)"
fi
echo ""

# Summary
echo "=================================="
echo "Summary"
echo "=================================="

DOCKER_OK=false
MINIKUBE_OK=false
KUBECTL_OK=false
HELM_OK=false

if command -v docker &> /dev/null && docker ps &> /dev/null; then
    DOCKER_OK=true
fi

if command -v minikube &> /dev/null && [ "$MINIKUBE_STATUS" = "Running" ]; then
    MINIKUBE_OK=true
fi

if command -v kubectl &> /dev/null && kubectl cluster-info &> /dev/null; then
    KUBECTL_OK=true
fi

if command -v helm &> /dev/null && helm list &> /dev/null; then
    HELM_OK=true
fi

if $DOCKER_OK && $MINIKUBE_OK && $KUBECTL_OK && $HELM_OK; then
    success "All required tools are working correctly!"
    echo ""
    echo "You can proceed with:"
    echo "  1. Build images: ./scripts/build-images.sh"
    echo "  2. Deploy: ./scripts/deploy.sh dev"
elif $DOCKER_OK && ! $MINIKUBE_OK; then
    warning "Docker is ready, but Minikube needs to be started"
    echo ""
    echo "Run: ./scripts/setup-minikube.sh"
elif ! $DOCKER_OK; then
    error "Docker is not accessible"
    echo ""
    echo "Enable Docker Desktop WSL integration:"
    echo "  Settings → Resources → WSL Integration → Enable your Ubuntu distro"
else
    warning "Some tools are not ready. See details above."
fi

echo ""
echo "=================================="
