document.addEventListener('DOMContentLoaded', function() {
      const calendarEl = document.getElementById('calendar');
      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        dateClick: function(info) {
          // Перевірка: чи дата з поточного місяця
          const clicked = info.date;
          const current = calendar.getDate();
          if (clicked.getFullYear() !== current.getFullYear() ||
              clicked.getMonth() !== current.getMonth()) {
            return;
          }

          // Прибираємо попередній вибір
          document.querySelectorAll('.fc-daygrid-day').forEach(day => {
            day.classList.remove('selected-date');
          });

          // Додаємо клас вибраній клітинці
          info.dayEl.classList.add('selected-date');

          // Виводимо дату
        //   alert('Вибрана дата: ' + info.dateStr);
        }
      });

      calendar.render();
    });