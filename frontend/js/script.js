// Highlight the selected time slot
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
    });
});