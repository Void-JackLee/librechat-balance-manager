import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],

  server: {
    port: 3010,
    proxy: {
      '/api': {
        target: 'http://localhost:3490', // 你的后端接口地址
        // changeOrigin: true,             // 允许跨域
      }
    }
  }
})
