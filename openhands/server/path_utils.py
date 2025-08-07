"""Path utilities for handling subpath routing."""
import os


def get_base_path() -> str:
    """Get the base path for the application.

    Returns the base path with leading and trailing slashes.
    Example: /kk/c3/openhands/ or / for root
    """
    base_path = os.getenv('OPENHANDS_BASE_PATH', '')
    if not base_path:
        return '/'

    # Ensure it starts and ends with /
    if not base_path.startswith('/'):
        base_path = '/' + base_path
    if not base_path.endswith('/'):
        base_path = base_path + '/'

    return base_path


def get_root_path() -> str:
    """Get the root path for FastAPI.

    Returns the base path without trailing slash for FastAPI root_path.
    Example: /kk/c3/openhands or empty string for root
    """
    base_path = get_base_path()
    if base_path == '/':
        return ''
    return base_path.rstrip('/')
