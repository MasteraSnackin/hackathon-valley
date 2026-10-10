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

export default defineConfig({
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
})
