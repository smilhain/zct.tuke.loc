// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if(!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if(sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}

// Получить элемент <span> с ID "temperature-value"
const temperatureValue = document.getElementById('temperature-value');
const humidityValue = document.getElementById('humidity-value');
const dateValue = document.getElementById('date-value');

// Отправить GET-запрос к серверу Flask для получения последней записи
fetch('/last_record')
  .then(response => response.json())
  .then(data => {
    // Заполнить значение <span> с последней записью
    temperatureValue.innerText = data.temperature;
    humidityValue.innerText = data.humidity;
    dateValue.innerText = data.date;
});

