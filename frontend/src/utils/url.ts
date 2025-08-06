/**
 * Utility functions for handling subpath configuration
 */

/**
 * Get the application base path from various sources
 * Priority: 1. Vite's BASE_URL (build time), 2. document.baseURI (runtime), 3. fallback to "/"
 */
export function getBasePath(): string {
  // In Vite builds, import.meta.env.BASE_URL is available
  if (typeof import.meta !== "undefined" && import.meta?.env?.BASE_URL) {
    return import.meta.env.BASE_URL;
  }

  // Fallback: derive from document.baseURI
  if (typeof document !== "undefined" && document.baseURI) {
    try {
      const url = new URL(document.baseURI);
      const path = url.pathname;
      return path === "/" ? "/" : path;
    } catch {
      // Fallback if URL parsing fails
    }
  }

  return "/";
}

/**
 * Get the API base URL for making HTTP requests
 */
export function getApiBaseUrl(): string {
  const basePath = getBasePath();
  const { protocol } = window.location;
  const { host } = window.location;

  // Remove trailing slash from base path for consistent URL construction
  const cleanBasePath = basePath === "/" ? "" : basePath.replace(/\/$/, "");

  return `${protocol}//${host}${cleanBasePath}`;
}

/**
 * Get the WebSocket base URL for WebSocket connections
 * Returns host only for socket.io compatibility
 */
export function getWebSocketBaseUrl(): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  const { host } = window.location;

  // For socket.io, we only return the host, not the full URL with path
  // The path will be handled by socket.io configuration
  return `${protocol}//${host}`;
}

/**
 * Get the WebSocket path for socket.io connections
 */
export function getWebSocketPath(): string {
  const basePath = getBasePath();
  const cleanBasePath = basePath === "/" ? "" : basePath.replace(/\/$/, "");
  return `${cleanBasePath}/socket.io/`;
}

/**
 * Construct a URL relative to the application base path
 */
export function resolveUrl(path: string): string {
  const basePath = getBasePath();

  // Ensure path starts with /
  const cleanPath = path.startsWith("/") ? path : `/${path}`;

  // If base path is root, just return the path
  if (basePath === "/") {
    return cleanPath;
  }

  // Remove trailing slash from base path and combine
  const cleanBasePath = basePath.replace(/\/$/, "");
  return `${cleanBasePath}${cleanPath}`;
}
