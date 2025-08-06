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
from openhands.server.static import SPAStaticFiles

# Get configurable base path from environment, default to root
OPENHANDS_BASE_PATH = os.getenv('OPENHANDS_BASE_PATH', '/')

# Validate and normalize the base path
if OPENHANDS_BASE_PATH and not isinstance(OPENHANDS_BASE_PATH, str):
    raise ValueError("OPENHANDS_BASE_PATH must be a string")

# Check for potentially dangerous characters
if OPENHANDS_BASE_PATH and any(char in OPENHANDS_BASE_PATH for char in ['<', '>', '"', "'", '&']):
    raise ValueError("OPENHANDS_BASE_PATH contains invalid characters")

# Ensure it starts with / and ends with /
if not OPENHANDS_BASE_PATH.startswith('/'):
    OPENHANDS_BASE_PATH = '/' + OPENHANDS_BASE_PATH
OPENHANDS_BASE_PATH = OPENHANDS_BASE_PATH.rstrip('/') + '/'
if OPENHANDS_BASE_PATH == '//':
    OPENHANDS_BASE_PATH = '/'

if os.getenv('SERVE_FRONTEND', 'true').lower() == 'true':
    base_app.mount(
        OPENHANDS_BASE_PATH, SPAStaticFiles(directory='./frontend/build', html=True), name='dist'
    )

base_app.add_middleware(LocalhostCORSMiddleware)
base_app.add_middleware(CacheControlMiddleware)
base_app.add_middleware(
    RateLimitMiddleware,
    rate_limiter=InMemoryRateLimiter(requests=10, seconds=1),
)

app = socketio.ASGIApp(sio, other_asgi_app=base_app)
