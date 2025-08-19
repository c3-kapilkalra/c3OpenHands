import os

import socketio

from openhands.server.app import app as base_app
from openhands.server.listen_socket import sio
from openhands.server.middleware import (
    CacheControlMiddleware,
    InMemoryRateLimiter,
    LocalhostCORSMiddleware,
    RateLimitMiddleware,
)
from openhands.server.path_utils import get_base_path, get_root_path
from openhands.server.static import SPAStaticFiles

if os.getenv('SERVE_FRONTEND', 'true').lower() == 'true':
    # When using root_path, FastAPI strips the prefix, so mount at root
    # When not using root_path, mount at the full base path
    mount_path = '/' if get_root_path() else get_base_path()
    base_app.mount(
        mount_path, SPAStaticFiles(directory='./frontend/build', html=True), name='dist'
    )

base_app.add_middleware(LocalhostCORSMiddleware)
base_app.add_middleware(CacheControlMiddleware)

# Configure rate limiting based on environment variables
rate_limit_enabled = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
if rate_limit_enabled:
    rate_limit_requests = int(os.getenv('RATE_LIMIT_REQUESTS', '10'))
    rate_limit_seconds = int(os.getenv('RATE_LIMIT_SECONDS', '1'))
    base_app.add_middleware(
        RateLimitMiddleware,
        rate_limiter=InMemoryRateLimiter(requests=rate_limit_requests, seconds=rate_limit_seconds),
    )


class SocketIOSubpathMiddleware:
    """Middleware to handle socket.io subpath routing with ASGI wrapper."""
    
    def __init__(self, app, socket_io_app):
        self.app = app
        self.socket_io_app = socket_io_app
        self.root_path = get_root_path()
    
    async def __call__(self, scope, receive, send):
        # Handle socket.io WebSocket connections with subpath support
        if scope["type"] == "websocket":
            path = scope.get("path", "")
            # Check if this is a socket.io request under the subpath
            if self.root_path and path.startswith(self.root_path + "/socket.io"):
                # Rewrite the path for socket.io by removing the root_path prefix
                scope = dict(scope)
                scope["path"] = path[len(self.root_path):]
                scope["root_path"] = self.root_path
                return await self.socket_io_app(scope, receive, send)
            elif not self.root_path and path.startswith("/socket.io"):
                # No subpath, direct socket.io connection
                return await self.socket_io_app(scope, receive, send)
        
        # For all other requests, use the main app
        return await self.app(scope, receive, send)

# Create custom ASGI app with proper subpath handling
socket_io_asgi = socketio.ASGIApp(sio, other_asgi_app=None)
app = SocketIOSubpathMiddleware(base_app, socket_io_asgi)
