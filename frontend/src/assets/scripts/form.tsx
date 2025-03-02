import React, { useState } from 'react';
import Calendar from './calendar';
import GlobalConfig from '../../config/globalConfig';

interface FormData {
  region: string;
  comuna: string;
  area: string;
  specialty: string;
  time_range_filter: string;
}

interface Slot {
  id: number;
  start_time: string;
  end_time: string;
}

const Formulario = () => {
  const [formData, setFormData] = useState<FormData>({
    region: '',
    comuna: '',
    area: '',
    specialty: '',
    time_range_filter: '',
  });
  const [availableSlots, setAvailableSlots] = useState<Slot[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Datos enviados:', formData);

    // Convertimos formData a un objeto compatible con URLSearchParams
    const queryParams = new URLSearchParams({
      region: formData.region,
      comuna: formData.comuna,
      area: formData.area,
      specialty: formData.specialty,
      time_range_filter: formData.time_range_filter,
    }).toString();
    const url = `${GlobalConfig.api.endpoints.availabilityCheck}?${queryParams}`;

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Datos recibidos del servidor:', data);
        setAvailableSlots(data.available_slots);
        alert('¡Solicitud enviada con éxito!');
      } else {
        const errorText = await response.text();
        console.error('Error en la respuesta:', response.status, errorText);
        alert(`Hubo un error al enviar la solicitud: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert('Error al conectar con el servidor. Revisa la consola para más detalles.');
    }
  };

  return (
    <div className="head">
      <form onSubmit={handleSubmit}>
        <div className="head-container">
          <div className="tittles">
            <h2>Región</h2>
            <div className="select">
              <select name="region" value={formData.region} onChange={handleChange}>
                <option value="" disabled>Región</option>
                <option value="1">Option 1</option>
                <option value="option-2">Option 2</option>
              </select>
            </div>
          </div>
          <div className="tittles">
            <h2>Comuna</h2>
            <div className="select">
              <select name="comuna" value={formData.comuna} onChange={handleChange}>
                <option value="" disabled>Comuna</option>
                <option value="1">Option 1</option>
                <option value="option-2">Option 2</option>
              </select>
            </div>
          </div>
          <div className="tittles">
            <h2>Area</h2>
            <div className="select">
              <select name="area" value={formData.area} onChange={handleChange}>
                <option value="" disabled>Area</option>
                <option value="3">Option 1</option>
                <option value="option-2">Option 2</option>
              </select>
            </div>
          </div>
          <div className="tittles">
            <h2>Especialidad</h2>
            <div className="select">
              <select name="specialty" value={formData.specialty} onChange={handleChange}>
                <option value="" disabled>Especialidad</option>
                <option value="trauma">Trauma</option>
                <option value="option-2">Option 2</option>
              </select>
            </div>
          </div>
          <div className="tittles">
            <h2>Time</h2>
            <div className="select">
              <select name="time_range_filter" value={formData.time_range_filter} onChange={handleChange}>
                <option value="" disabled>Schedule</option>
                <option value="afternoon">Afternoon</option>
                <option value="morning">Morning</option>
              </select>
            </div>
          </div>
          <div className="tittles">
            <h2>Language</h2>
            <div className="select">
              <select name="language">
                <option value="" disabled>Language</option>
                <option value="spanish">Spanish</option>
                <option value="english">English</option>
              </select>
            </div>
          </div>
          <div className="form-button">
          <button type="submit" className='find'><i className="fa-solid fa-magnifying-glass"></i> Buscar Hora</button>
        </div>
        </div>
        
      </form>
      <Calendar availableSlots={availableSlots} />
    </div>
  );
};

export default Formulario;