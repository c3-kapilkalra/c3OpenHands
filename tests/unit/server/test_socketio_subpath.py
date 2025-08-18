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


def test_socketio_path_construction():
    """Test that socket.io path is constructed correctly for various base paths."""
    test_cases = [
        ('/', '/socket.io'),
        ('/api/', '/api/socket.io'),
        ('/test-subpath/', '/test-subpath/socket.io'),
        ('/nested/path/', '/nested/path/socket.io'),
    ]
    
    for base_path, expected_socket_path in test_cases:
        with patch.dict(os.environ, {'OPENHANDS_BASE_PATH': base_path}):
            from openhands.server.path_utils import get_base_path
            
            # Simulate the path construction logic from shared.py
            constructed_path = get_base_path().rstrip('/') + '/socket.io'
            assert constructed_path == expected_socket_path


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