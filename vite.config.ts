import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import myPlugin from './src/plugins/build-info-plugin'

export default defineConfig({
  server: {
    port: 8885,
  },
  plugins: [
    react(),
    myPlugin({
      injectGlobal: true,
      reportFileName: 'build-info.json',
      enableGitInfo: false,
    }),
  ],
})
