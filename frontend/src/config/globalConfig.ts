// Variables de entorno
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_BASE_VER = import.meta.env.VITE_API_BASE_VER || '/api/v1';

// Tipos para los endpoints
interface ApiEndpoints {
  availabilityCheck: string;
  appointments: string;
}

// Configuraciones globales
const GlobalConfig = {
  api: {
    baseUrl: API_BASE_URL,
    baseVersion: API_BASE_VER,
    endpoints: {
      availabilityCheck: `${API_BASE_URL}${API_BASE_VER}/availability/check/`,
      appointments: `${API_BASE_URL}${API_BASE_VER}/appointments/`,
    } as ApiEndpoints,
  },
};

export default GlobalConfig;