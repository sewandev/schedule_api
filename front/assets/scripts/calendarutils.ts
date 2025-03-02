import { useState, useEffect } from 'react';

export interface Slot {
  id: number;
  start_time: string;
  end_time: string;
}

export interface Day {
  number: number;
  isActive: boolean;
  isFocus: boolean;
  isCurrentMonth: boolean;
  isAvailable?: boolean;
  availableHours?: { start: string; end: string }[]; // Horas en formato "HH:MM"
}

export interface CalendarState {
  currentDate: Date;
  displayedMonth: Date;
  days: Day[];
}

export const useCalendar = (availableSlots: Slot[] = []) => {
  const today = new Date();
  const [calendarState, setCalendarState] = useState<CalendarState>({
    currentDate: today,
    displayedMonth: today,
    days: generateDays(today, today, availableSlots),
  });

  useEffect(() => {
    setCalendarState((prev) => ({
      ...prev,
      days: generateDays(prev.currentDate, prev.displayedMonth, availableSlots),
    }));
  }, [availableSlots]);

  const getMonthYearString = (date: Date): string => {
    return date.toLocaleString('default', { month: 'long', year: 'numeric' });
  };

  function generateDays(currentDate: Date, displayMonth: Date, availableSlots: Slot[]): Day[] {
    const daysInMonth = new Date(displayMonth.getFullYear(), displayMonth.getMonth() + 1, 0).getDate();
    const firstDayOfMonth = new Date(displayMonth.getFullYear(), displayMonth.getMonth(), 1).getDay();
    const daysInPrevMonth = new Date(displayMonth.getFullYear(), displayMonth.getMonth(), 0).getDate();

    const days: Day[] = [];

    // Procesar las fechas y horas disponibles desde availableSlots
    const availableDatesMap = availableSlots.reduce((map, slot) => {
      const date = new Date(slot.start_time);
      const dateString = date.toDateString();
      const startTime = slot.start_time.slice(11, 16); // "HH:MM" desde ISO
      const endTime = slot.end_time.slice(11, 16); // "HH:MM" desde ISO

      if (!map[dateString]) {
        map[dateString] = [];
      }
      map[dateString].push({ start: startTime, end: endTime });
      return map;
    }, {} as Record<string, { start: string; end: string }[]>);

    console.log('Fechas y horas procesadas:', availableDatesMap);

    // Días del mes anterior
    const prevMonthYear = displayMonth.getMonth() === 0 ? displayMonth.getFullYear() - 1 : displayMonth.getFullYear();
    const prevMonth = displayMonth.getMonth() === 0 ? 11 : displayMonth.getMonth() - 1;

    for (let i = firstDayOfMonth - 1; i >= 0; i--) {
      const dayNumber = daysInPrevMonth - i;
      const date = new Date(prevMonthYear, prevMonth, dayNumber);
      const dateString = date.toDateString();
      const isFocus =
        date.getDate() === currentDate.getDate() &&
        date.getMonth() === currentDate.getMonth() &&
        date.getFullYear() === currentDate.getFullYear();
      const isActive = date >= currentDate || isFocus;
      const isAvailable = !!availableDatesMap[dateString];
      const availableHours = availableDatesMap[dateString] || [];

      days.push({ number: dayNumber, isActive, isFocus, isCurrentMonth: false, isAvailable, availableHours });
    }

    // Días del mes actual
    for (let i = 1; i <= daysInMonth; i++) {
      const date = new Date(displayMonth.getFullYear(), displayMonth.getMonth(), i);
      const dateString = date.toDateString();
      const isFocus =
        date.getDate() === currentDate.getDate() &&
        date.getMonth() === currentDate.getMonth() &&
        date.getFullYear() === currentDate.getFullYear();
      const isActive = date >= currentDate || isFocus;
      const isAvailable = !!availableDatesMap[dateString];
      const availableHours = availableDatesMap[dateString] || [];

      days.push({ number: i, isActive, isFocus, isCurrentMonth: true, isAvailable, availableHours });
    }

    // Días del próximo mes
    const totalDays = days.length;
    const remainingDays = (7 - (totalDays % 7)) % 7;
    const nextMonthYear = displayMonth.getMonth() === 11 ? displayMonth.getFullYear() + 1 : displayMonth.getFullYear();
    const nextMonth = displayMonth.getMonth() === 11 ? 0 : displayMonth.getMonth() + 1;

    if (remainingDays > 0) {
      for (let i = 1; i <= remainingDays; i++) {
        const date = new Date(nextMonthYear, nextMonth, i);
        const dateString = date.toDateString();
        const isFocus =
          date.getDate() === currentDate.getDate() &&
          date.getMonth() === currentDate.getMonth() &&
          date.getFullYear() === currentDate.getFullYear();
        const isActive = date >= currentDate || isFocus;
        const isAvailable = !!availableDatesMap[dateString];
        const availableHours = availableDatesMap[dateString] || [];

        days.push({ number: i, isActive, isFocus, isCurrentMonth: false, isAvailable, availableHours });
      }
    }

    return days;
  }

  const handlePrevMonth = () => {
    setCalendarState((prev) => {
      const newMonth = new Date(prev.displayedMonth);
      newMonth.setMonth(newMonth.getMonth() - 1);
      return {
        ...prev,
        displayedMonth: newMonth,
        days: generateDays(prev.currentDate, newMonth, availableSlots),
      };
    });
  };

  const handleNextMonth = () => {
    setCalendarState((prev) => {
      const newMonth = new Date(prev.displayedMonth);
      newMonth.setMonth(newMonth.getMonth() + 1);
      return {
        ...prev,
        displayedMonth: newMonth,
        days: generateDays(prev.currentDate, newMonth, availableSlots),
      };
    });
  };

  return {
    monthYear: getMonthYearString(calendarState.displayedMonth),
    days: calendarState.days,
    handlePrevMonth,
    handleNextMonth,
  };
};