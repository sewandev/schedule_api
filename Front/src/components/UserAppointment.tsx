import { useState } from 'react';
import Calendar from 'react-calendar';
import 'react-calendar/dist/Calendar.css';

type Value = Date | [Date, Date] | null; // Se incluye null

interface Slot {
  start_time: string;
  end_time: string;
}

interface UserAppointmentProps {
  slots: Slot[];
}

export function UserAppointment({ slots }: UserAppointmentProps) {
  const [date, setDate] = useState<Value>(new Date());
  const [showModal, setShowModal] = useState(false);
  const [selectedSlots, setSelectedSlots] = useState<Slot[]>([]);

  const availableDates = slots.map((slot) => new Date(slot.start_time).toDateString());

  const tileContent = ({ date, view }: { date: Date; view: string }) => {
    if (view === 'month' && availableDates.includes(date.toDateString())) {
      return <span className="text-green-500">●</span>;
    }
    return null;
  };

  const onDateClick = (value: Date) => {
    const daySlots = slots.filter(
      (slot) => new Date(slot.start_time).toDateString() === value.toDateString()
    );
    setSelectedSlots(daySlots);
    setShowModal(true);
  };

  // Se actualiza la función para aceptar dos parámetros
  const handleDateChange = (
    value: Value,
    _event: React.MouseEvent<HTMLButtonElement, MouseEvent>
  ) => {
    setDate(value); // Puede ser Date, [Date, Date] o null
  };

  return (
    <div className="relative">
      <Calendar
        onChange={handleDateChange}
        value={date}
        tileContent={tileContent}
        onClickDay={onDateClick}
        className="border-none shadow-lg rounded-lg"
      />
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white p-6 rounded-lg shadow-xl max-w-sm w-full">
            <h3 className="text-xl font-bold mb-4">
              Horas disponibles -{' '}
              {date instanceof Date
                ? date.toLocaleDateString()
                : Array.isArray(date)
                ? date[0].toLocaleDateString()
                : 'Fecha seleccionada'}
            </h3>
            {selectedSlots.length > 0 ? (
              <ul className="space-y-2">
                {selectedSlots.map((slot, idx) => (
                  <li key={idx} className="p-2 bg-gray-100 rounded">
                    {new Date(slot.start_time).toLocaleTimeString()} -{' '}
                    {new Date(slot.end_time).toLocaleTimeString()}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500">No hay horas disponibles</p>
            )}
            <button
              onClick={() => setShowModal(false)}
              className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Cerrar
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
