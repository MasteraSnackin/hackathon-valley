import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// The FastAPI backend (app/main.py) rejects any non-GET request whose Origin
// header doesn't match its own base URL — a plain proxy isn't enough because
// the browser still sends Origin: http://localhost:5173. We rewrite the
// outgoing Origin header to the backend's own origin before forwarding, so
// its same-origin check passes. This is dev-tooling only; no backend file is
// touched.
const BACKEND = 'http://127.0.0.1:8017'

// `npm run build` writes into the backend's static directory so FastAPI serves
// the dashboard at /dashboard on the same origin as the API (no proxy, no
// CORS). Stable file names keep rebuilds as small, reviewable diffs.
export default defineConfig(({ command }) => ({
  base: command === 'build' ? '/static/dashboard/' : '/',
  build: {
    outDir: '../static/dashboard',
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: 'assets/[name].js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: 'assets/[name][extname]',
      },
    },
  },
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: BACKEND,
        changeOrigin: true,
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq) => {
            proxyReq.setHeader('origin', BACKEND)
          })
        },
      },
    },
  },
}))
