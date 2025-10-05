document.addEventListener('DOMContentLoaded', function() {

const tg = window.Telegram?.WebApp;

if (tg) {
  console.log("✅ Telegram WebApp підключено");
  tg.expand(); // щоб відкрилося на весь екран
} else {
  console.log("❌ Telegram WebApp не знайдено");
}



  const calendarEl = document.getElementById('calendar');
  const monthLabel = document.getElementById('month-label');

  const today = new Date();
  const calendar = new FullCalendar.Calendar(calendarEl, {
    headerToolbar: false,
    contentHeight: 'auto',
  });

  calendar.render();

  function updateMonthLabel() {
    const date = calendar.getDate();
    const monthNames = [
      "Січень","Лютий","Березень","Квітень","Травень","Червень",
      "Липень","Серпень","Вересень","Жовтень","Листопад","Грудень"
    ];
    monthLabel.textContent = monthNames[date.getMonth()] + " " + date.getFullYear();
  }

  updateMonthLabel();

  // кнопка "назад" — блокуємо минулі місяці
  document.getElementById('prev').addEventListener('click', () => {
    const currentDate = calendar.getDate();
    const prevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
    if (prevMonth >= new Date(today.getFullYear(), today.getMonth(), 1)) {
      calendar.prev();
      updateMonthLabel();
    }
  });

  // кнопка "вперед"
  document.getElementById('next').addEventListener('click', () => {
    calendar.next();
    updateMonthLabel();
  });

  // Ініціалізуємо Telegram WebApp (якщо є)
  

  // Вибір дати
  calendarEl.addEventListener('click', function(e) {
    const dayCell = e.target.closest('.fc-daygrid-day');
    if (dayCell) {
      document.querySelectorAll('.fc-daygrid-day').forEach(day => {
        day.classList.remove('selected-date');
      });
      dayCell.classList.add('selected-date');
      const data = (dayCell.textContent.trim() + ' ' + monthLabel.textContent);

      if (tg) {
        tg.sendData(JSON.stringify({ date: data }));
        tg.close();
      } else {
        console.log("Дата вибрана:", data); // для тестів у браузері
      }
    }
  });
});

