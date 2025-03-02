import React, { useState } from 'react';
import { useCalendar, Day, Slot } from './calendarutils';
import GlobalConfig from '../../config/globalConfig';

interface CalendarProps {
  availableSlots: Slot[];
}

const Calendar: React.FC<CalendarProps> = ({ availableSlots }) => {
  const { monthYear, days, handlePrevMonth, handleNextMonth } = useCalendar(availableSlots);
  const [selectedDay, setSelectedDay] = useState<Day | null>(null);
  const [popupPosition, setPopupPosition] = useState<{ x: number; y: number } | null>(null);
  const [selectedHour, setSelectedHour] = useState<string>(''); // Estado para la hora seleccionada en el popup
  const [confirmedTasks, setConfirmedTasks] = useState<Record<string, string[]>>({}); // Almacena tareas confirmadas por día

  const weeks: Array<Day[]> = [];
  for (let i = 0; i < days.length; i += 7) {
    weeks.push(days.slice(i, i + 7));
  }

  const handleDayClick = (day: Day, event: React.MouseEvent<HTMLDivElement>) => {
    if (day.isAvailable) {
      setSelectedDay(day);
      setSelectedHour(day.availableHours?.[0] ? `${day.availableHours[0].start}-${day.availableHours[0].end}` : ''); // Selecciona la primera hora por defecto
      const rect = event.currentTarget.getBoundingClientRect();
      setPopupPosition({ x: rect.left, y: rect.bottom + window.scrollY });
    }
  };

  const closePopup = () => {
    setSelectedDay(null);
    setPopupPosition(null);
    setSelectedHour('');
  };

  const handleHourChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedHour(e.target.value);
  };

  const handleConfirm = () => {
    if (selectedDay && selectedHour) {
      const dayKey = `${monthYear}-${selectedDay.number}`; // Clave única para el día
      setConfirmedTasks((prev) => ({
        ...prev,
        [dayKey]: [...(prev[dayKey] || []), selectedHour], // Agrega la hora confirmada
      }));
      closePopup(); // Cierra el popup tras confirmar
    }
  };

  const handleSendAppointments = async () => {
    const appointments = Object.entries(confirmedTasks).flatMap(([dayKey, tasks]) => {
      const [, dayNumber] = dayKey.split('-'); // Extraemos solo el número del día
      const day = parseInt(dayNumber, 10);

      return tasks.map((task) => {
        // Buscar el slot original que coincida con el día y la hora seleccionada
        const slot = availableSlots.find((s) => {
          const slotDate = new Date(s.start_time);
          const slotStartTime = s.start_time.slice(11, 16); // "HH:MM" desde ISO
          const slotEndTime = s.end_time.slice(11, 16); // "HH:MM" desde ISO
          const taskTime = `${slotStartTime}-${slotEndTime}`;
          
          // Comparar el día exacto
          const matchesDay = slotDate.getDate() === day && 
                            slotDate.getMonth() === new Date(availableSlots[0].start_time).getMonth() && 
                            slotDate.getFullYear() === new Date(availableSlots[0].start_time).getFullYear();
          const matchesTime = taskTime === task; // "09:00-10:00" === "09:00-10:00"
          
          console.log('Comparando slot:', { slotStartTime, slotEndTime, task, matchesDay, matchesTime });
          return matchesDay && matchesTime;
        });

        if (!slot) {
          console.error('No se encontró un slot correspondiente para:', { dayKey, task });
          return null;
        }

        // Añadir milisegundos al formato ISO
        const startTimeWithMs = slot.start_time.includes('.') ? slot.start_time : `${slot.start_time}.000`;
        const endTimeWithMs = slot.end_time.includes('.') ? slot.end_time : `${slot.end_time}.000`;

        return {
          id: slot.id, // Usar el ID original del slot en lugar de 0
          patient_id: Math.floor(Math.random() * 2) + 1, // Random entre 1 y 10
          start_time: startTimeWithMs, // Usar el start_time con milisegundos
          end_time: endTimeWithMs, // Usar el end_time con milisegundos
        };
      }).filter(Boolean); // Filtrar nulls por si no se encuentra un slot
    });

    if (appointments.length === 0) {
      alert('No hay citas confirmadas válidas para enviar.');
      return;
    }

    // Enviar solo el primer appointment como objeto
    const appointmentToSend = appointments[0];

    try {
      const url = GlobalConfig.api.endpoints.appointments;
      console.log('Datos enviados:', JSON.stringify(appointmentToSend, null, 2)); // Log para depurar
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(appointmentToSend), // Enviar un solo objeto
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Respuesta del servidor:', data);
        alert('¡Citas enviadas con éxito!');
      } else {
        const errorText = await response.text();
        console.error('Error en la respuesta:', response.status, errorText);
        alert(`Hubo un error al enviar las citas: ${response.status} - ${errorText}`);
      }
    } catch (error) {
      console.error('Error de conexión:', error);
      alert('Error al conectar con el servidor. Revisa la consola para más detalles.');
    }
  };

  return (
    <>
      <div className="date">
        <div className="date-container">
          <div className="month-year">
            <h3>{monthYear}</h3>
          </div>
          <div className="text">
            <p>Set your weekly hours</p>
          </div>
        </div>
        <div className="date-arrows">
          <div className="arrow-l" onClick={handlePrevMonth}>
            <i className="fa-solid fa-chevron-left"></i>
          </div>
          <div className="arrow-r" onClick={handleNextMonth}>
            <i className="fa-solid fa-chevron-right"></i>
          </div>
        </div>
      </div>
      <div className="month">
        <div className="text-week">
          {['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'].map((day) => (
            <div className="text-day" key={day}>
              <h1>{day}</h1>
            </div>
          ))}
        </div>
        {weeks.map((week, weekIndex) => (
          <div className="week" key={weekIndex}>
            {week.map((day) => {
              const dayKey = `${monthYear}-${day.number}`;
              const tasks = confirmedTasks[dayKey] || [];
              const dayClasses = [
                'day',
                day.isActive ? 'active' : '',
                day.isFocus ? 'focus' : '',
                !day.isCurrentMonth ? 'outside-month' : '',
                day.isAvailable ? 'available' : '',
              ].filter(Boolean).join(' ');

              return (
                <div
                  className={dayClasses}
                  key={`${weekIndex}-${day.number}`}
                  onClick={(e) => handleDayClick(day, e)}
                >
                  <div className="number">{day.number}</div>
                  {tasks.map((task, index) => (
                    <div className="task" key={index}>
                      {task}
                    </div>
                  ))}
                </div>
              );
            })}
          </div>
        ))}
      </div>

      {selectedDay && popupPosition && (
        <div className='background-popup'>
          <div className="available-hour">                      
              <div className="popup-content">
                <h4>Horas {selectedDay.number} de {monthYear}</h4>
                <select value={selectedHour} onChange={handleHourChange}>
                  {selectedDay.availableHours && selectedDay.availableHours.length > 0 ? (
                    selectedDay.availableHours.map((hour, index) => (
                      <option key={index} value={`${hour.start}-${hour.end}`}>
                        {hour.start} - {hour.end}
                      </option>
                    ))
                  ) : (
                    <option disabled><h1>No hay horas disponibles</h1></option>
                  )}
                </select>
                <div className='onclick-buttons'>
                  <button className='confirm' onClick={handleConfirm}>Confirmar</button>
                  <button className='cancel' onClick={closePopup}>Cerrar</button>
                </div>
              </div>
            </div>
        </div>
      )}

      <div className="c-buttons" style={{ marginTop: '20px', textAlign: 'center' }}>
        <button onClick={handleSendAppointments}>Enviar</button>
      </div>
    </>
  );
};

export default Calendar;