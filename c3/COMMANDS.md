# C3 OpenHands - Useful Commands

This document contains frequently used commands for building, deploying, and managing the C3 OpenHands application.

## 🐳 Docker Commands

### Build & Push Commands

```bash
# Build the Docker image
docker build -t c3openhands/c3-openhands:latest .

# Build with specific tag
docker build -t c3openhands/c3-openhands:0.51.1 .

# Tag for Google Container Registry
docker tag c3openhands/c3-openhands:latest us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:latest
docker tag c3openhands/c3-openhands:0.51.1 us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1

# Push to Google Container Registry
docker push us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:latest
docker push us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1

# One-liner: Build, tag, and push
docker build -t c3openhands/c3-openhands:0.51.1 . && \
docker tag c3openhands/c3-openhands:0.51.1 us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1 && \
docker push us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1
```

### Local Development

```bash
# Run locally with subpath
docker run -d \
  -e OPENHANDS_BASE_PATH="/c3/c3openhands/" \
  -e RATE_LIMIT_ENABLED="false" \
  -p 3000:3000 \
  c3openhands/c3-openhands:latest

# Run locally at root path
docker run -d \
  -p 3000:3000 \
  c3openhands/c3-openhands:latest

# Run with debug logs
docker run -d \
  -e DEBUG="1" \
  -e LOG_ALL_EVENTS="true" \
  -p 3000:3000 \
  c3openhands/c3-openhands:latest
```

### Docker Cleanup

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -a -f

# Remove all unused resources
docker system prune -a -f

# Check disk usage
docker system df
```

## ☸️ Kubernetes Commands

### Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
kubectl get ingress

# Check specific deployment
kubectl describe deployment cs-10101010
kubectl logs -f deployment/cs-10101010

# Get pod logs
kubectl logs -f pod/cs-10101010-xxx-xxx

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Debugging

```bash
# Shell into running pod
kubectl exec -it deployment/cs-10101010 -- /bin/bash

# Port forward for local access
kubectl port-forward deployment/cs-10101010 3000:3000

# Check pod resources
kubectl top pods
kubectl describe pod cs-10101010-xxx-xxx

# Check persistent volumes
kubectl get pv
kubectl get pvc
```

### Updates

```bash
# Update deployment with new image
kubectl set image deployment/cs-10101010 openhands=us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1

# Restart deployment
kubectl rollout restart deployment/cs-10101010

# Check rollout status
kubectl rollout status deployment/cs-10101010

# Rollback deployment
kubectl rollout undo deployment/cs-10101010
```

## 🔧 Development Commands

### Frontend

```bash
# Install dependencies
cd frontend && npm install

# Development with subpath
export VITE_APP_BASE_URL="/c3/c3openhands/"
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Build for subpath
cd frontend && VITE_APP_BASE_URL="/c3/c3openhands/" npm run build:subpath
```

### Backend

```bash
# Install Python dependencies
poetry install

# Run backend locally
make start-backend

# Run with debug
DEBUG=1 make start-backend

# Run tests
make test
```

## 🌐 Environment Variables

### Development
```bash
export VITE_APP_BASE_URL="/c3/c3openhands/"
export VITE_BACKEND_HOST="127.0.0.1:3000"
export VITE_USE_TLS="false"
```

### Production/Kubernetes
```bash
OPENHANDS_BASE_PATH="/c3/c3openhands/"
RATE_LIMIT_ENABLED="false"
DEBUG="1"
LOG_ALL_EVENTS="true"
```

## 🔍 Troubleshooting

### Common Issues

```bash
# Check if containers are running
docker ps

# Check container logs
docker logs container_name

# Check Kubernetes pod status
kubectl get pods -o wide

# Check ingress configuration
kubectl describe ingress cs-10101010-ingress

# Test connectivity
curl -I http://aksleslie.c3ci.cloud/kk/c3/openhands/health

# Check rate limiting (if enabled)
curl -v http://localhost:3000/api/models
```

### Health Checks

```bash
# Local health check
curl http://localhost:3000/health

# Kubernetes health check (with subpath)
curl http://aksleslie.c3ci.cloud/kk/c3/openhands/health

# Check if assets are loading
curl -I http://aksleslie.c3ci.cloud/kk/c3/openhands/assets/
```

## 📝 Quick Reference

| Command | Description |
|---------|-------------|
| `make build` | Build the application |
| `make start-backend` | Start backend development server |
| `cd frontend && npm run dev` | Start frontend development server |
| `docker system prune -f` | Clean up Docker resources |
| `kubectl get pods` | Check Kubernetes pod status |
| `kubectl logs -f deployment/cs-10101010` | Follow deployment logs |

---

*Last updated: 2025-08-06*
