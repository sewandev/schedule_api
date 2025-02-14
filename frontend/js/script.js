const timeButtons = document.querySelectorAll('.times button');

        timeButtons.forEach(button => {
            button.addEventListener('click', () => {
                timeButtons.forEach(btn => btn.style.backgroundColor = '#007acc');
                button.style.backgroundColor = '#ffa500';
            });
        });

        // Handle calendar navigation
        const prevWeek = document.getElementById('prev-week');
        const nextWeek = document.getElementById('next-week');
        const days = document.querySelectorAll('.calendar .day');
        const appointmentTitle = document.getElementById('appointment-title');

        prevWeek.addEventListener('click', () => {
            alert('Semana anterior');
        });

        nextWeek.addEventListener('click', () => {
            alert('Semana siguiente');
        });

        days.forEach(day => {
            day.addEventListener('click', () => {
                days.forEach(d => d.classList.remove('active'));
                day.classList.add('active');
                const dayText = day.textContent.split('\n')[0];
                const dateText = day.textContent.split('\n')[1];
                appointmentTitle.textContent = `${dayText} ${dateText} de Febrero`;
            });
        });

        // Highlight today if present
        const today = new Date().getDate();
        days.forEach(day => {
            if (parseInt(day.dataset.date) === today) {
                day.classList.add('active');
                const dayText = day.textContent.split('\n')[0];
                const dateText = day.textContent.split('\n')[1];
                appointmentTitle.textContent = `${dayText} ${dateText} de Febrero`;
            }
        });