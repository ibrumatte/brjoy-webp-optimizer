import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import legacy from '@vitejs/plugin-legacy'

export default defineConfig({
  base: './',
  plugins: [
    react(),
    legacy({
      targets: ['defaults', 'Firefox >= 78', 'Chrome >= 64'],
      renderLegacyChunks: true,
      modernPolyfills: true,
    }),
  ],
  build: {
    outDir: 'dist',
    emptyOutDir: true
  }
})
