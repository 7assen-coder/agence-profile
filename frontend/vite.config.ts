import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiProxy =
    env.VITE_PROXY_TARGET ?? 'http://127.0.0.1:5001'

  return {
    plugins: [react(), tailwindcss()],
    server: {
      port: 5174,
      strictPort: false,
      proxy: {
        '/api': {
          target: apiProxy,
          changeOrigin: true,
        },
      },
    },
  }
})
