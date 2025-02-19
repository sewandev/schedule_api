document.addEventListener('DOMContentLoaded', () => {
    const calendar = document.getElementById('calendar');
    const slotsContainer = document.getElementById('slots');

    // Función para generar el calendario mensual
    function generateCalendar(year, month) {
        const date = new Date(year, month, 1);
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDay = date.getDay();

        calendar.innerHTML = '';
        slotsContainer.innerHTML = '';

        for (let i = 0; i < firstDay; i++) {
            calendar.innerHTML += '<div class="day"></div>';
        }

        for (let day = 1; day <= daysInMonth; day++) {
            const dayElement = document.createElement('div');
            dayElement.classList.add('day');
            dayElement.textContent = day;
            dayElement.dataset.date = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            calendar.appendChild(dayElement);
        }
    }

    // Función para pintar días disponibles
    function highlightAvailableDays(availableSlots) {
        document.querySelectorAll('.day').forEach(day => {
            const dayDate = day.dataset.date;
            if (availableSlots.some(slot => slot.slots.some(s => s.start_time.startsWith(dayDate)))) {
                day.classList.add('available');
                day.addEventListener('click', () => showSlots(dayDate, availableSlots));
            }
        });
    }

    // Función para mostrar horarios
    function showSlots(date, availableSlots) {
        slotsContainer.innerHTML = '';
        const medic = availableSlots.find(m => m.slots.some(s => s.start_time.startsWith(date)));
        if (medic) {
            medic.slots.forEach(slot => {
                if (slot.start_time.startsWith(date)) {
                    const div = document.createElement('div');
                    div.classList.add('slot');
                    div.textContent = `${new Date(slot.start_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} - ${new Date(slot.end_time).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
                    slotsContainer.appendChild(div);
                }
            });
        }
    }

    function fetchAvailability() {
        fetch('http://127.0.0.1:8000/api/v1/availability/check/?region=1&comuna=1&area=3&specialty=Trauma')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                generateCalendar(2025, 1); // Febrero de 2025 (enero es 0)
                highlightAvailableDays(data.available_slots);
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
                // Aquí podrías mostrar un mensaje de error en la UI si quieres
            });
    }

    // Iniciar la carga de datos desde la API
    fetchAvailability();
});