import { useState } from 'react';
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { DateClickArg } from '@fullcalendar/interaction';

interface Slot {
  start_time: string;
  end_time: string;
}

interface UserAppointmentProps {
  slots: Slot[];
}

export function UserAppointment({ slots }: UserAppointmentProps) {
  const [showModal, setShowModal] = useState(false);
  const [selectedDateSlots, setSelectedDateSlots] = useState<Slot[]>([]);

  // Obtener fechas únicas disponibles (distinct)
  const uniqueDates = Array.from(
    new Set(slots.map((slot) => new Date(slot.start_time).toDateString()))
  ).map((dateStr) => new Date(dateStr));

  // Generar eventos con "Disponibilidad" para los días únicos
  const events = uniqueDates.map((date) => ({
    title: 'Disponibilidad',
    start: date,
    allDay: true, // Evento de día completo
    backgroundColor: 'transparent', // Fondo transparente para que coincida con el día
    borderColor: 'transparent', // Sin borde
    textColor: '#0f766e', // Teal oscuro para el texto
    extendedProps: { date }, // Guardamos la fecha para filtrar slots
  }));

  // Estilizar días disponibles y deshabilitar días anteriores
  const dayCellClassNames = (arg: { date: Date; view: { type: string } }) => {
    const isAvailable = uniqueDates.some(
      (d) => d.toDateString() === arg.date.toDateString()
    );
    const isPast = arg.date < new Date(); // Días anteriores al actual

    if (arg.view.type === 'dayGridMonth') {
      if (isPast && !isAvailable) {
        return 'bg-gray-100 text-gray-400 cursor-not-allowed'; // Días anteriores sin disponibilidad
      }
      if (isAvailable) {
        return 'bg-gradient-to-br from-teal-100 to-teal-300 text-teal-800 font-semibold transition-all duration-300 hover:bg-teal-400 hover:shadow-lg rounded-lg cursor-pointer';
      }
    }
    return '';
  };

  // Manejar clic en un día
  const handleDateClick = (info: DateClickArg) => {
    const clickedDate = info.date;
    const isAvailable = uniqueDates.some(
      (d) => d.toDateString() === clickedDate.toDateString()
    );

    if (isAvailable) {
      const daySlots = slots.filter(
        (slot) =>
          new Date(slot.start_time).toDateString() === clickedDate.toDateString()
      );
      setSelectedDateSlots(daySlots);
      setShowModal(true);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto p-6 bg-white shadow-xl rounded-xl text-gray-800">
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        dateClick={handleDateClick}
        dayCellClassNames={dayCellClassNames} // Estilos personalizados
        eventClassNames="pointer-events-none" // Permitir que el clic pase al día
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: '',
        }}
        height={700} // Tamaño grande
        titleFormat={{ year: 'numeric', month: 'long' }}
        buttonText={{
          today: 'Hoy',
          month: 'Mes',
        }}
        locale="es"
        firstDay={1}
        dayHeaderClassNames="text-gray-700 font-semibold"
      />

      {/* Modal con lista completa de fechas y horas */}
      {showModal && selectedDateSlots.length > 0 && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 transition-opacity duration-300">
          <div className="bg-white p-6 rounded-xl shadow-2xl max-w-md w-full transform transition-all duration-300 scale-100">
            <h3 className="text-xl font-bold mb-4 bg-teal-500 text-white p-3 rounded-t-lg">
              Horas disponibles -{' '}
              {new Date(selectedDateSlots[0].start_time).toLocaleDateString(
                'es-ES',
                {
                  weekday: 'long',
                  day: 'numeric',
                  month: 'long',
                }
              )}
            </h3>
            <div className="max-h-64 overflow-y-auto space-y-3">
              {selectedDateSlots.map((slot, idx) => (
                <div
                  key={idx}
                  className="p-3 bg-teal-50 rounded-lg shadow-sm hover:bg-teal-100 transition-colors duration-200"
                >
                  <p className="text-teal-800">
                    {new Date(slot.start_time).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}{' '}
                    -{' '}
                    {new Date(slot.end_time).toLocaleTimeString([], {
                      hour: '2-digit',
                      minute: '2-digit',
                    })}
                  </p>
                </div>
              ))}
            </div>
            <button
              onClick={() => setShowModal(false)}
              className="mt-6 w-full py-2 bg-teal-500 text-white rounded-lg hover:bg-teal-600 transition-colors duration-200"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}