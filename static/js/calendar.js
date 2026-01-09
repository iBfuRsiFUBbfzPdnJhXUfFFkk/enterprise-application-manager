// Calendar Application
// Handles rendering and interaction for the calendar views

// State management
const calendarState = {
    currentView: 'month',
    currentDate: new Date(),
    events: [],
    activeFilters: ['maintenance', 'release', 'sprint', 'request', 'meeting']
};

// Initialize calendar on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeCalendar();
    setupEventListeners();
});

function initializeCalendar() {
    // Load view preference from localStorage
    const savedView = localStorage.getItem('calendarView');
    if (savedView) {
        calendarState.currentView = savedView;
        updateViewButtons();
    }

    // Fetch and render calendar
    fetchAndRenderCalendar();
}

function setupEventListeners() {
    // View switcher buttons
    document.querySelectorAll('.view-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const view = e.target.dataset.view;
            switchView(view);
        });
    });

    // Event type filters
    document.querySelectorAll('.event-filter').forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            const eventType = e.target.dataset.type;
            if (e.target.checked) {
                if (!calendarState.activeFilters.includes(eventType)) {
                    calendarState.activeFilters.push(eventType);
                }
            } else {
                calendarState.activeFilters = calendarState.activeFilters.filter(t => t !== eventType);
            }
            renderCalendar();
        });
    });

    // Navigation buttons
    document.getElementById('prev-period').addEventListener('click', () => navigatePeriod(-1));
    document.getElementById('next-period').addEventListener('click', () => navigatePeriod(1));
    document.getElementById('today-btn').addEventListener('click', () => {
        calendarState.currentDate = new Date();
        fetchAndRenderCalendar();
    });
}

function switchView(view) {
    calendarState.currentView = view;
    localStorage.setItem('calendarView', view);
    updateViewButtons();
    fetchAndRenderCalendar();
}

function updateViewButtons() {
    document.querySelectorAll('.view-btn').forEach(btn => {
        if (btn.dataset.view === calendarState.currentView) {
            btn.classList.remove('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
            btn.classList.add('bg-indigo-600', 'text-white');
        } else {
            btn.classList.remove('bg-indigo-600', 'text-white');
            btn.classList.add('bg-gray-200', 'text-gray-700', 'hover:bg-gray-300');
        }
    });
}

function navigatePeriod(direction) {
    const date = new Date(calendarState.currentDate);

    switch (calendarState.currentView) {
        case 'month':
            date.setMonth(date.getMonth() + direction);
            break;
        case 'week':
            date.setDate(date.getDate() + (7 * direction));
            break;
        case 'day':
            date.setDate(date.getDate() + direction);
            break;
        case 'agenda':
            date.setMonth(date.getMonth() + direction);
            break;
    }

    calendarState.currentDate = date;
    fetchAndRenderCalendar();
}

function fetchAndRenderCalendar() {
    const { startDate, endDate } = getDateRange();
    const types = calendarState.activeFilters.join(',');

    const url = `/authenticated/calendar/api/events/?start=${startDate}&end=${endDate}&types=${types}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            calendarState.events = data.events || [];
            renderCalendar();
        })
        .catch(error => {
            console.error('Error fetching calendar events:', error);
            showError('Failed to load calendar events');
        });
}

function getDateRange() {
    const date = new Date(calendarState.currentDate);
    let startDate, endDate;

    switch (calendarState.currentView) {
        case 'month':
            startDate = new Date(date.getFullYear(), date.getMonth(), 1);
            endDate = new Date(date.getFullYear(), date.getMonth() + 1, 0);
            break;
        case 'week':
            const dayOfWeek = date.getDay();
            startDate = new Date(date);
            startDate.setDate(date.getDate() - dayOfWeek);
            endDate = new Date(startDate);
            endDate.setDate(startDate.getDate() + 6);
            break;
        case 'day':
            startDate = new Date(date);
            endDate = new Date(date);
            break;
        case 'agenda':
            startDate = new Date(date);
            endDate = new Date(date);
            endDate.setMonth(endDate.getMonth() + 2);
            break;
    }

    return {
        startDate: formatDate(startDate),
        endDate: formatDate(endDate)
    };
}

function formatDate(date) {
    return date.toISOString().split('T')[0];
}

function renderCalendar() {
    updatePeriodLabel();

    switch (calendarState.currentView) {
        case 'month':
            renderMonthView();
            break;
        case 'week':
            renderWeekView();
            break;
        case 'day':
            renderDayView();
            break;
        case 'agenda':
            renderAgendaView();
            break;
    }
}

function updatePeriodLabel() {
    const date = calendarState.currentDate;
    let label = '';

    switch (calendarState.currentView) {
        case 'month':
            label = date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
            break;
        case 'week':
            const weekStart = new Date(date);
            weekStart.setDate(date.getDate() - date.getDay());
            const weekEnd = new Date(weekStart);
            weekEnd.setDate(weekStart.getDate() + 6);
            label = `${weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${weekEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
            break;
        case 'day':
            label = date.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });
            break;
        case 'agenda':
            label = 'Upcoming Events';
            break;
    }

    document.getElementById('current-period').textContent = label;
}

function renderMonthView() {
    const container = document.getElementById('calendar-grid');
    const date = new Date(calendarState.currentDate);
    const year = date.getFullYear();
    const month = date.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDate = new Date(firstDay);
    startDate.setDate(startDate.getDate() - startDate.getDay());

    const days = [];
    const currentDate = new Date(startDate);

    for (let i = 0; i < 42; i++) {
        days.push(new Date(currentDate));
        currentDate.setDate(currentDate.getDate() + 1);
    }

    let html = '<div class="grid grid-cols-7 gap-1">';

    // Header
    ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(day => {
        html += `<div class="text-center font-semibold text-gray-700 py-2 text-sm">${day}</div>`;
    });

    // Days
    days.forEach(day => {
        const isCurrentMonth = day.getMonth() === month;
        const isToday = isDateToday(day);
        const dayEvents = getEventsForDate(day);

        html += `<div class="border border-gray-200 min-h-[100px] p-2 ${isCurrentMonth ? 'bg-white' : 'bg-gray-50'}">`;
        html += `<div class="text-sm font-medium ${isToday ? 'bg-indigo-600 text-white rounded-full w-6 h-6 flex items-center justify-center' : isCurrentMonth ? 'text-gray-900' : 'text-gray-400'}">${day.getDate()}</div>`;

        if (dayEvents.length > 0) {
            const displayEvents = dayEvents.slice(0, 3);
            displayEvents.forEach(event => {
                html += `<div class="mt-1 text-xs px-1 py-0.5 rounded truncate cursor-pointer hover:opacity-80" style="background-color: ${event.color}; color: white;" onclick="window.location='${event.detail_url}'" title="${event.title}">${event.title}</div>`;
            });

            if (dayEvents.length > 3) {
                html += `<div class="mt-1 text-xs text-gray-600">+${dayEvents.length - 3} more</div>`;
            }
        }

        html += '</div>';
    });

    html += '</div>';
    container.innerHTML = html;
}

function renderWeekView() {
    const container = document.getElementById('calendar-grid');
    const date = new Date(calendarState.currentDate);
    const dayOfWeek = date.getDay();
    const weekStart = new Date(date);
    weekStart.setDate(date.getDate() - dayOfWeek);

    const days = [];
    for (let i = 0; i < 7; i++) {
        const day = new Date(weekStart);
        day.setDate(weekStart.getDate() + i);
        days.push(day);
    }

    let html = '<div class="overflow-x-auto"><table class="min-w-full"><thead><tr>';

    days.forEach(day => {
        const isToday = isDateToday(day);
        html += `<th class="text-center py-2 border-b-2 ${isToday ? 'bg-indigo-50' : ''}">
            <div class="text-sm font-semibold text-gray-700">${day.toLocaleDateString('en-US', { weekday: 'short' })}</div>
            <div class="text-lg font-bold ${isToday ? 'text-indigo-600' : 'text-gray-900'}">${day.getDate()}</div>
        </th>`;
    });

    html += '</tr></thead><tbody><tr>';

    days.forEach(day => {
        const dayEvents = getEventsForDate(day);
        html += `<td class="border border-gray-200 p-2 align-top min-w-[150px]">`;

        dayEvents.forEach(event => {
            html += `<div class="mb-2 p-2 rounded text-xs cursor-pointer hover:opacity-80" style="background-color: ${event.color}; color: white;" onclick="window.location='${event.detail_url}'">
                <div class="font-semibold">${event.title}</div>
                ${!event.all_day ? `<div class="mt-1">${formatTime(event.start)}</div>` : ''}
            </div>`;
        });

        html += '</td>';
    });

    html += '</tr></tbody></table></div>';
    container.innerHTML = html;
}

function renderDayView() {
    const container = document.getElementById('calendar-grid');
    const dayEvents = getEventsForDate(calendarState.currentDate);

    let html = '<div class="space-y-2">';

    if (dayEvents.length === 0) {
        html += '<div class="text-center py-12 text-gray-500">No events scheduled for this day</div>';
    } else {
        dayEvents.forEach(event => {
            html += `<div class="p-4 rounded-lg cursor-pointer hover:opacity-80" style="background-color: ${event.color}; color: white;" onclick="window.location='${event.detail_url}'">
                <div class="font-bold text-lg">${event.title}</div>
                <div class="mt-1">${formatTime(event.start)}${event.end ? ' - ' + formatTime(event.end) : ''}</div>
                ${event.description ? `<div class="mt-2 text-sm">${event.description}</div>` : ''}
            </div>`;
        });
    }

    html += '</div>';
    container.innerHTML = html;
}

function renderAgendaView() {
    const container = document.getElementById('calendar-grid');
    const sortedEvents = [...calendarState.events].sort((a, b) =>
        new Date(a.start) - new Date(b.start)
    );

    if (sortedEvents.length === 0) {
        container.innerHTML = '<div class="text-center py-12 text-gray-500">No upcoming events</div>';
        return;
    }

    let html = '<div class="space-y-1">';
    let currentDate = null;

    sortedEvents.forEach(event => {
        const eventDate = new Date(event.start);
        const dateStr = eventDate.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

        if (dateStr !== currentDate) {
            currentDate = dateStr;
            html += `<div class="font-bold text-gray-900 mt-4 mb-2 pt-4 border-t border-gray-200 first:mt-0 first:pt-0 first:border-t-0">${dateStr}</div>`;
        }

        html += `<div class="flex items-center p-3 rounded-lg hover:bg-gray-50 cursor-pointer" onclick="window.location='${event.detail_url}'">
            <div class="w-3 h-3 rounded-full mr-3" style="background-color: ${event.color};"></div>
            <div class="flex-1">
                <div class="font-medium text-gray-900">${event.title}</div>
                ${!event.all_day ? `<div class="text-sm text-gray-600">${formatTime(event.start)}</div>` : ''}
            </div>
        </div>`;
    });

    html += '</div>';
    container.innerHTML = html;
}

function getEventsForDate(date) {
    const dateStr = formatDate(date);
    return calendarState.events.filter(event => {
        const eventStart = event.start.split('T')[0];
        const eventEnd = event.end ? event.end.split('T')[0] : eventStart;
        return dateStr >= eventStart && dateStr <= eventEnd;
    });
}

function isDateToday(date) {
    const today = new Date();
    return date.getDate() === today.getDate() &&
           date.getMonth() === today.getMonth() &&
           date.getFullYear() === today.getFullYear();
}

function formatTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
}

function showError(message) {
    const container = document.getElementById('calendar-grid');
    container.innerHTML = `<div class="text-center py-12 text-red-600">${message}</div>`;
}
