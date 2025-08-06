# C3 OpenHands - Useful Commands

This document contains frequently used commands for building, deploying, and managing the C3 OpenHands application.


# Build and Run the Docker image locally
```bash
docker build -t openhands:latest -f containers/app/Dockerfile .
docker run --rm -e OPENHANDS_BASE_PATH="/c3/c3/openhands/" -e SANDBOX_RUNTIME_CONTAINER_IMAGE=docker.all-hands.dev/all-hands-ai/runtime:0.51-nikolaik -e LOG_ALL_EVENTS=true -v /var/run/docker.sock:/var/run/docker.sock -v ~/.openhands:/.openhands -p 3000:3000 --add-host host.docker.internal:host-gateway --name openhands-app openhands:latest
```

# Build and Publish the docker image for production
```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t us-west1-docker.pkg.dev/cicd-360621/docker/c3openhands/c3-openhands:0.51.1 \
  -f containers/app/Dockerfile \
  --push .
```

# Version is defined here
`pyproject.toml`
