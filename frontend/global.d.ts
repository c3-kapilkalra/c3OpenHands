interface Window {
  __APP_MODE__?: "saas" | "oss";
  __GITHUB_CLIENT_ID__?: string | null;
}

interface ImportMetaEnv {
  readonly BASE_URL: string;
  readonly VITE_BACKEND_BASE_URL?: string;
  // Add other VITE_ variables as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
