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

app = socketio.ASGIApp(sio, other_asgi_app=base_app)
