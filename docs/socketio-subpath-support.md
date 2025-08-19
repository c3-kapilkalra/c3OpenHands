# Socket.IO Subpath Support

This document explains how socket.io connections are configured to work with subpaths in OpenHands, ensuring consistent behavior with API routes and frontend API calls.

## Overview

OpenHands supports serving the application under custom subpaths (e.g., `/api/openhands/`, `/kk/c3/openhands/`) for reverse proxy and multi-tenant deployments. Socket.io connections must be properly configured to work under these subpaths.

## Implementation

### Backend Configuration

The socket.io server is configured in `openhands/server/shared.py` with the `path` parameter:

```python
from openhands.server.path_utils import get_base_path

sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    client_manager=client_manager,
    max_http_buffer_size=4 * 1024 * 1024,
    # Use subpath for socket.io connections to align with API routes
    path=get_base_path().rstrip('/') + '/socket.io',
)
```

This ensures that:
- When `OPENHANDS_BASE_PATH="/"` → socket.io endpoint is `/socket.io`
- When `OPENHANDS_BASE_PATH="/api/"` → socket.io endpoint is `/api/socket.io`
- When `OPENHANDS_BASE_PATH="/kk/c3/openhands/"` → socket.io endpoint is `/kk/c3/openhands/socket.io`

### Frontend Configuration

The socket.io client is configured in `frontend/src/context/ws-client-provider.tsx` to use the subpath:

```typescript
// Get the base path from Vite's BASE_URL for socket.io subpath support
const basePath = (import.meta.env.BASE_URL || '/').replace(/\/+$/, '');
const socketPath = basePath + '/socket.io';

sio = io(baseUrl, {
  transports: ["websocket"],
  query,
  path: socketPath,
});
```

This ensures the client connects to the correct socket.io endpoint based on the build-time configuration.

## Environment Variables

### Backend
- `OPENHANDS_BASE_PATH`: Sets the base path for the application (e.g., `/api/`, `/kk/c3/openhands/`)

### Frontend
- `VITE_APP_BASE_URL`: Used during development to set the base URL
- `BASE_URL`: Set by Vite during build time, used by the socket.io client for path construction

## Deployment Examples

### Docker with Subpath
```bash
docker run -e OPENHANDS_BASE_PATH="/api/" openhands:latest
```

### Kubernetes with Ingress
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: openhands
        env:
        - name: OPENHANDS_BASE_PATH
          value: "/kk/c3/openhands/"
```

### Nginx Reverse Proxy
```nginx
location /api/ {
    proxy_pass http://openhands:3000/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## Testing

Tests are included to verify subpath functionality:

- Backend: `tests/unit/server/test_socketio_subpath.py`
- Frontend: `frontend/__tests__/context/ws-client-provider.test.tsx`

Run tests:
```bash
# Backend tests
python -m pytest tests/unit/server/test_socketio_subpath.py

# Frontend tests
cd frontend && npm test -- ws-client-provider.test.tsx
```

## Troubleshooting

### Connection Issues
1. Verify `OPENHANDS_BASE_PATH` is set correctly on the backend
2. Ensure the frontend is built with the correct `BASE_URL`
3. Check that reverse proxy routes include socket.io endpoints

### Path Mismatches
- Backend socket.io path should match `${OPENHANDS_BASE_PATH}/socket.io`
- Frontend should use the same base path from `BASE_URL`
- Both should result in the same absolute socket.io endpoint URL