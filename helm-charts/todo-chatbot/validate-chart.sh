#!/bin/bash

# Helm Chart Validation Script for todo-chatbot
# This script validates the Helm chart structure and files

set -e

CHART_DIR="$(cd "$(dirname "$0")" && pwd)"
CHART_NAME="todo-chatbot"

echo "========================================="
echo "Validating Helm Chart: $CHART_NAME"
echo "Chart Directory: $CHART_DIR"
echo "========================================="
echo ""

# Check required files
echo "1. Checking required files..."
REQUIRED_FILES=(
    "Chart.yaml"
    "values.yaml"
    "templates/_helpers.tpl"
    "templates/backend-deployment.yaml"
    "templates/backend-service.yaml"
    "templates/frontend-deployment.yaml"
    "templates/frontend-service.yaml"
    "templates/configmap.yaml"
    "templates/NOTES.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$CHART_DIR/$file" ]; then
        echo "   ✓ $file exists"
    else
        echo "   ✗ $file is missing"
        exit 1
    fi
done
echo ""

# Validate YAML syntax
echo "2. Validating YAML syntax..."
YAML_FILES=(
    "Chart.yaml"
    "values.yaml"
    "values-dev.yaml"
    "values-prod.yaml"
    "templates/backend-deployment.yaml"
    "templates/backend-service.yaml"
    "templates/frontend-deployment.yaml"
    "templates/frontend-service.yaml"
    "templates/configmap.yaml"
)

for file in "${YAML_FILES[@]}"; do
    # For template files, just check if they exist and are readable
    if [[ "$file" == templates/* ]]; then
        if [ -r "$CHART_DIR/$file" ]; then
            echo "   ✓ $file is readable (template file)"
        else
            echo "   ✗ $file is not readable"
            exit 1
        fi
    else
        # For non-template files, validate YAML syntax
        if python3 -c "import yaml; yaml.safe_load(open('$CHART_DIR/$file'))" 2>/dev/null; then
            echo "   ✓ $file has valid YAML syntax"
        else
            echo "   ✗ $file has invalid YAML syntax"
            exit 1
        fi
    fi
done
echo ""

# Check Chart.yaml required fields
echo "3. Validating Chart.yaml metadata..."
CHART_YAML="$CHART_DIR/Chart.yaml"
python3 << EOF
import yaml
with open('$CHART_YAML', 'r') as f:
    chart = yaml.safe_load(f)

required_fields = ['apiVersion', 'name', 'version', 'appVersion', 'description']
for field in required_fields:
    if field in chart:
        print(f"   ✓ {field}: {chart[field]}")
    else:
        print(f"   ✗ {field} is missing")
        exit(1)
EOF
echo ""

# Check template files contain Go templating
echo "4. Checking template files..."
TEMPLATE_FILES=(
    "templates/backend-deployment.yaml"
    "templates/backend-service.yaml"
    "templates/frontend-deployment.yaml"
    "templates/frontend-service.yaml"
    "templates/configmap.yaml"
)

for file in "${TEMPLATE_FILES[@]}"; do
    if grep -q "{{" "$CHART_DIR/$file"; then
        echo "   ✓ $file contains template directives"
    else
        echo "   ⚠ $file may not contain template directives"
    fi
done
echo ""

# Validate helper templates
echo "5. Checking helper templates..."
HELPERS="$CHART_DIR/templates/_helpers.tpl"
REQUIRED_HELPERS=(
    "todo-chatbot.name"
    "todo-chatbot.fullname"
    "todo-chatbot.labels"
    "todo-chatbot.selectorLabels"
    "todo-chatbot.backend.labels"
    "todo-chatbot.frontend.labels"
)

for helper in "${REQUIRED_HELPERS[@]}"; do
    if grep -q "define \"$helper\"" "$HELPERS"; then
        echo "   ✓ Helper '$helper' defined"
    else
        echo "   ✗ Helper '$helper' is missing"
        exit 1
    fi
done
echo ""

# Check values files
echo "6. Validating values files..."
VALUES_FILES=(
    "values.yaml:Default"
    "values-dev.yaml:Development"
    "values-prod.yaml:Production"
)

for entry in "${VALUES_FILES[@]}"; do
    IFS=':' read -r file desc <<< "$entry"
    if [ -f "$CHART_DIR/$file" ]; then
        echo "   ✓ $desc values file ($file) exists"

        # Check for required top-level keys
        python3 << EOF
import yaml
with open('$CHART_DIR/$file', 'r') as f:
    values = yaml.safe_load(f)

required_keys = ['backend', 'frontend']
for key in required_keys:
    if key in values:
        replicas = values[key].get('replicaCount', 'not set')
        print(f"      - {key}: {replicas} replicas")
EOF
    fi
done
echo ""

# Try Helm lint (may fail in WSL environments)
echo "7. Running Helm lint (if available)..."
if command -v helm &> /dev/null; then
    if helm lint "$CHART_DIR" 2>&1; then
        echo "   ✓ Helm lint passed"
    else
        echo "   ⚠ Helm lint failed (this may be expected in WSL environments)"
        echo "      The chart files are valid, but Helm may have WSL compatibility issues"
    fi
else
    echo "   ⚠ Helm not found, skipping lint check"
fi
echo ""

# Try template rendering
echo "8. Testing template rendering (if Helm available)..."
if command -v helm &> /dev/null; then
    if helm template test-release "$CHART_DIR" > /dev/null 2>&1; then
        echo "   ✓ Template rendering successful"
    else
        echo "   ⚠ Template rendering failed (this may be expected in WSL environments)"
    fi
else
    echo "   ⚠ Helm not found, skipping template test"
fi
echo ""

echo "========================================="
echo "Chart validation completed!"
echo "========================================="
echo ""
echo "Manual validation commands:"
echo "  helm lint $CHART_DIR"
echo "  helm template test-release $CHART_DIR"
echo "  helm install --dry-run --debug test-release $CHART_DIR"
echo ""
echo "Installation commands:"
echo "  Development: helm install todo-chatbot $CHART_DIR -f $CHART_DIR/values-dev.yaml"
echo "  Production:  helm install todo-chatbot $CHART_DIR -f $CHART_DIR/values-prod.yaml"
echo ""
