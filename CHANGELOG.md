# Changelog

## [0.51.1] - 2025-08-06

### **Backend API Subpath Support Fix**

**Fixed**: API endpoints now properly accessible under configured subpaths, resolving 404 errors for routes like `/api/options/config`.

**Key Changes**:
- Added FastAPI `root_path` configuration for subpath deployments
- Fixed static file mounting when using `root_path` - mount at `/` instead of full subpath
- **Fixed frontend API baseURL** to include subpath from `import.meta.env.BASE_URL`
- Created shared `path_utils.py` module to consolidate base path logic
- API routes now correctly respond under configured `OPENHANDS_BASE_PATH`

**Impact**: Completes the subpath implementation from v0.51.1 by fixing both backend API routing and frontend API calls under subpaths.

**Deployment Note**: Ensure `OPENHANDS_BASE_PATH` includes trailing slash (e.g., `/kk/c3/openhands/`) for Kubernetes deployments.

## [0.51.1] - 2025-08-06

### **Configurable Rate Limiting for Kubernetes Deployments**

**Added**: Environment variable controls for rate limiting to fix 429 "Too Many Requests" errors in Kubernetes environments.

**Key Features**:
- `RATE_LIMIT_ENABLED` environment variable to disable/enable rate limiting (default: `"true"`)
- `RATE_LIMIT_REQUESTS` to configure requests per time window (default: `10`)
- `RATE_LIMIT_SECONDS` to configure time window in seconds (default: `1`)
- Health check endpoints automatically excluded from rate limiting
- Subpath health checks (e.g., `/kk/c3/openhands/health`) excluded from rate limiting

**Usage**:
```yaml
# Kubernetes deployment - disable rate limiting
env:
  - name: RATE_LIMIT_ENABLED
    value: "false"

# Or increase limits
env:
  - name: RATE_LIMIT_REQUESTS
    value: "100"
  - name: RATE_LIMIT_SECONDS
    value: "1"
```

## [0.51.1] - 2025-08-05

### **Dynamic Subpath Configuration Support**

**Added**: Comprehensive support for serving OpenHands under custom subpaths (e.g., `/c3/c3openhands/`) for reverse proxy and multi-tenant deployments.

**Key Features**:
- Dynamic Vite proxy configuration that automatically handles any subpath
- Runtime Docker frontend rebuilds when `OPENHANDS_BASE_PATH` environment variable is set
- Single Docker image works with any subpath without rebuilding
- Backward compatible - existing root path deployments continue working unchanged

**Usage**: Set `VITE_APP_BASE_URL="/your-path/"` for development or `OPENHANDS_BASE_PATH="/your-path/"` for Docker deployments.
