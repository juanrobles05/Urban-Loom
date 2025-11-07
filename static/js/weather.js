/**
 * Weather Widget - Obtiene ubicación del usuario y muestra el clima
 */

class WeatherWidget {
    constructor() {
        this.defaultLocation = { lat: 6.2442, lng: -75.5812 }; // Medellín por defecto
        this.weatherContainer = null;
        this.init();
    }

    async init() {
        this.createWeatherContainer();
        await this.getLocationAndWeather();
        
        // Actualizar cada 30 minutos
        setInterval(() => {
            this.getLocationAndWeather();
        }, 30 * 60 * 1000);
    }

    createWeatherContainer() {
        // Encontrar el contenedor de idiomas en el navbar
        const languageSelector = document.querySelector('.flex.items-center.space-x-2');
        if (languageSelector) {
            // Crear el contenedor del clima
            this.weatherContainer = document.createElement('div');
            this.weatherContainer.className = 'flex items-center space-x-2 text-sm border-l border-gray-600 pl-4 ml-4';
            this.weatherContainer.innerHTML = `
                <div id="weather-info" class="flex items-center space-x-2">
                    <div class="animate-pulse">
                        <div class="h-4 bg-gray-600 rounded w-16"></div>
                    </div>
                </div>
            `;
            
            // Insertar antes del selector de idiomas
            languageSelector.parentNode.insertBefore(this.weatherContainer, languageSelector);
        }
    }

    async getLocationAndWeather() {
        try {
            const position = await this.getCurrentPosition();
            const lat = position.coords.latitude;
            const lng = position.coords.longitude;
            
            await this.fetchWeather(lat, lng);
        } catch (error) {
            console.log('No se pudo obtener la ubicación, usando Medellín por defecto');
            await this.fetchWeather(this.defaultLocation.lat, this.defaultLocation.lng);
        }
    }

    getCurrentPosition() {
        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                reject(new Error('Geolocalización no soportada'));
                return;
            }

            const options = {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 300000 // 5 minutos
            };

            navigator.geolocation.getCurrentPosition(resolve, reject, options);
        });
    }

    async fetchWeather(lat, lng) {
        try {
            const response = await fetch(`/api/weather/?lat=${lat}&lng=${lng}`);
            const data = await response.json();
            
            if (data.success) {
                this.updateWeatherDisplay(data);
            } else {
                this.showError('Error al obtener el clima');
            }
        } catch (error) {
            console.error('Error fetching weather:', error);
            this.showError('Sin conexión');
        }
    }

    updateWeatherDisplay(data) {
        const weatherInfo = document.getElementById('weather-info');
        if (!weatherInfo) return;

        const weather = data.weather;
        const location = data.location;
        
        // Icono del clima basado en condiciones
        const weatherIcon = this.getWeatherIcon(weather.weathercode, weather.is_day);
        
        weatherInfo.innerHTML = `
            <div class="flex items-center space-x-2 text-gray-300">
                <span class="text-lg">${weatherIcon}</span>
                <div class="flex flex-col">
                    <span class="text-xs font-medium text-white">${Math.round(weather.temperature)}${weather.temperature_unit}</span>
                    <span class="text-xs text-gray-400">${location.city}</span>
                </div>
            </div>
        `;

        // Tooltip con más información
        weatherInfo.title = `${weather.description}\nViento: ${weather.windspeed} ${weather.windspeed_unit}\nActualizado: ${new Date().toLocaleTimeString()}`;
    }

    showError(message) {
        const weatherInfo = document.getElementById('weather-info');
        if (!weatherInfo) return;

        weatherInfo.innerHTML = `
            <div class="flex items-center space-x-1 text-gray-500">
                <span class="text-sm">🌤️</span>
                <span class="text-xs">${message}</span>
            </div>
        `;
    }

    getWeatherIcon(weatherCode, isDay) {
        const icons = {
            // Despejado
            0: isDay ? '☀️' : '🌙',
            
            // Parcialmente nublado
            1: isDay ? '🌤️' : '🌙',
            2: isDay ? '⛅' : '☁️',
            3: '☁️',
            
            // Niebla
            45: '🌫️',
            48: '🌫️',
            
            // Llovizna
            51: '🌦️',
            53: '🌦️',
            55: '🌦️',
            56: '🌧️',
            57: '🌧️',
            
            // Lluvia
            61: '🌧️',
            63: '🌧️',
            65: '🌧️',
            66: '🌧️',
            67: '🌧️',
            
            // Nieve
            71: '❄️',
            73: '❄️',
            75: '❄️',
            77: '🌨️',
            
            // Aguaceros
            80: '🌦️',
            81: '🌦️',
            82: '🌧️',
            
            // Nevadas
            85: '🌨️',
            86: '🌨️',
            
            // Tormentas
            95: '⛈️',
            96: '⛈️',
            99: '⛈️'
        };
        
        return icons[weatherCode] || (isDay ? '🌤️' : '🌙');
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new WeatherWidget();
});
