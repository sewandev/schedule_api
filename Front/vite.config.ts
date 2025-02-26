import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0', // Permite que la app sea accesible desde otras redes
    port: 5173,      // Puerto en el que se ejecutará la app
    strictPort: true, // Asegura que el puerto especificado sea utilizado
    open: true,       // Abre automáticamente la app en el navegador (opcional)
  },
});