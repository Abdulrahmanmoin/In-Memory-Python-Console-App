@echo off
REM Rebuild frontend Docker image with correct backend URL for Kubernetes
REM This script rebuilds the frontend with NEXT_PUBLIC_API_URL set to the NodePort backend service

echo Building frontend Docker image with backend URL: http://localhost:30800

cd frontend

docker build --build-arg NEXT_PUBLIC_API_URL=http://localhost:30800 -t todo-frontend:v1.0.0 .

if %ERRORLEVEL% EQU 0 (
  echo.
  echo ✓ Frontend image rebuilt successfully
  echo ✓ Backend URL: http://localhost:30800
  echo.
  echo Next steps:
  echo 1. Deploy/upgrade the Helm chart
  echo 2. The frontend will now call the backend via NodePort ^(localhost:30800^)
) else (
  echo ✗ Build failed
  exit /b 1
)

cd ..
