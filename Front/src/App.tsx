import { useEffect, useState } from 'react';
import { fetchAvailability } from './lib/api';
import { AvailabilityResponse } from './types';
import { UserAppointment } from './components/UserAppointment';

function App() {
  const [availability, setAvailability] = useState<AvailabilityResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadAvailability = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchAvailability();
      setAvailability(data);
    } catch (err) {
      setError('¡Ups! Error al cargar la disponibilidad.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAvailability();
  }, []);

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-4">Disponibilidad de Médicos</h1>
      <button
        onClick={loadAvailability}
        disabled={isLoading}
        className="mb-6 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {isLoading ? 'Cargando...' : 'Recargar'}
      </button>
      {error && <div className="mb-4 text-red-500">{error}</div>}
      {isLoading && !availability ? (
        <div className="text-center text-gray-500">Cargando...</div>
      ) : (
        availability && (
          <UserAppointment slots={availability.available_slots[0].slots} />
        )
      )}
    </div>
  );
}
export default App;