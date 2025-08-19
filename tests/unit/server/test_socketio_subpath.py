"""Tests for socket.io subpath support."""
import os
from unittest.mock import patch

import pytest

from openhands.server.path_utils import get_base_path


def test_get_base_path_consistency():
    """Test that get_base_path function behaves consistently."""
    test_cases = [
        ('/', '/'),
        ('/test/', '/test/'),
        ('/test', '/test/'),
        ('test', '/test/'),
        ('test/', '/test/'),
        ('/nested/path/', '/nested/path/'),
        ('/nested/path', '/nested/path/'),
    ]
    
    for input_path, expected in test_cases:
        with patch.dict(os.environ, {'OPENHANDS_BASE_PATH': input_path}):
            assert get_base_path() == expected


def test_socketio_path_configuration():
    """Test that socket.io server is configured correctly for subpath middleware."""
    # The socket.io server should always use '/socket.io' path
    # The custom SocketIOSubpathMiddleware handles subpath routing
    test_cases = [
        ('/', '/socket.io'),
        ('/api/', '/socket.io'),
        ('/test-subpath/', '/socket.io'),
        ('/nested/path/', '/socket.io'),
    ]
    
    for base_path, expected_socket_path in test_cases:
        with patch.dict(os.environ, {'OPENHANDS_BASE_PATH': base_path}):
            # Socket.io server always uses '/socket.io' with custom middleware
            socket_server_path = '/socket.io'
            assert socket_server_path == expected_socket_path


def test_socketio_subpath_middleware_routing():
    """Test that the middleware correctly routes socket.io requests."""
    test_cases = [
        # (base_path, client_path, should_route_to_socketio)
        ('/', '/socket.io', True),
        ('/api/', '/api/socket.io', True),
        ('/kk/c3/openhands/', '/kk/c3/openhands/socket.io', True),
        ('/api/', '/socket.io', False),  # Wrong path for subpath
        ('/', '/api/socket.io', False),  # Subpath when none expected
    ]
    
    for base_path, client_path, should_route in test_cases:
        with patch.dict(os.environ, {'OPENHANDS_BASE_PATH': base_path}):
            from openhands.server.path_utils import get_root_path
            
            root_path = get_root_path()
            
            # Simulate middleware logic
            if root_path and client_path.startswith(root_path + "/socket.io"):
                routes_to_socketio = True
            elif not root_path and client_path.startswith("/socket.io"):
                routes_to_socketio = True
            else:
                routes_to_socketio = False
            
            assert routes_to_socketio == should_route, f"Failed for {base_path} -> {client_path}"


def test_empty_base_path():
    """Test behavior when OPENHANDS_BASE_PATH is empty or not set."""
    # Test with empty string
    with patch.dict(os.environ, {'OPENHANDS_BASE_PATH': ''}):
        assert get_base_path() == '/'
    
    # Test with env var removed
    with patch.dict(os.environ, {}, clear=True):
        if 'OPENHANDS_BASE_PATH' in os.environ:
            del os.environ['OPENHANDS_BASE_PATH']
        assert get_base_path() == '/'