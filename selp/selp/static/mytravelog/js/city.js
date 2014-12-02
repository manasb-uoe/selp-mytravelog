/**
 * Created by Manas on 01-12-2014.
 */

var TabNavigationHandler = (function () {

    function init() {
        // navigate to #info if no hash found
        if (window.location.hash == '') {
            window.location.href = window.location.href + '#info'
        }
        _navigateToActiveTab();

        // navigate to active tab every time the hash changes
        $(window).on('hashchange', function () {
            _navigateToActiveTab();
        });
    }

    function _navigateToActiveTab() {
        var hash = window.location.hash;

        // only mark selected tab as active
        var activeTab = $('a[href="' + hash +'"]');
        activeTab.siblings().removeClass('tab-active');
        activeTab.addClass('tab-active');

        // only show active tab content
        var activeContent = $('.' + hash.substr(1) + '-content');
        activeContent.show();
        activeContent.siblings('div[class$=content]').hide();
    }

    return {
        init: init
    };
}());

var WeatherForecastHandler = (function () {

    var _config = {
        cityName: $('.city-name').first().text(),
        baseApiUrl: 'http://api.openweathermap.org/data/2.5/forecast/daily?',
        weatherContainer: $('.weather-container'),
        baseWeatherIconUrl: 'http://openweathermap.org/img/w/'
    };

    function init() {
        _parseWeatherForecastJson();
    }

    function DayWeather(day, min, max, description, icon, humidity, windSpeed, cloudiness) {
        var daysOfAWeek = {
            0: "Sunday",
            1: "Monday",
            2: "Tuesday",
            3: "Wednesday",
            4: "Thursday",
            5: "Friday",
            6: "Saturday"
        };

        var currentDate = new Date();
        var today = currentDate.getDay();
        currentDate.setDate(currentDate.getDate() + 1);
        var tomorrow = currentDate.getDay();

        if (day == today) {
            this.day = "Today"
        }
        else if (day == tomorrow) {
            this.day = "Tomorrow"
        }
        else {
            this.day = daysOfAWeek[day];
        }
        this.min = min;
        this.max = max;
        this.description = description;
        this.icon = icon;
        this.humidity = humidity;
        this.windSpeed = windSpeed;
        this.cloudiness = cloudiness;
    }

    function _parseWeatherForecastJson() {
        var apiUrl = _config.baseApiUrl + "q=" + _config.cityName + "&mode=json&units=metric&cnt=7";

        $.ajax({
            url: apiUrl,
            type: 'GET',
            dataType: 'json',
            success: function (response) {
                var parsedData = [];
                var currentDate = new Date();
                var list =  response.list;
                for (var key in list) {
                    if (list.hasOwnProperty(key)) {
                        var listItem = list[key];
                        var temp = listItem.temp;
                        var weather = listItem.weather[0];

                        parsedData.push(new DayWeather(
                            currentDate.getDay(),
                            temp.min,
                            temp.max,
                            weather.description,
                            weather.icon,
                            listItem.humidity,
                            listItem.speed,
                            listItem.clouds
                        ));
                        currentDate.setDate(currentDate.getDate() + 1);
                    }
                }
                _showWeatherForecast(parsedData);
            }
        });
    }

    function _showWeatherForecast(parsedData) {
        for (var i=0; i<parsedData.length; i++) {
            var dayWeather = parsedData[i];
            var html = [
                '<div class="day-weather default-box-shadow">',
                '<div class="day-and-description-container">',
                '<p class="day">' + dayWeather.day + '</p>',
                '<p class="description">' + dayWeather.description + '</p>',
                '</div>',
                '<div class="icon-and-temp-container">',
                '<div class="icon-container">',
                '<img class="icon" src="' + _config.baseWeatherIconUrl + dayWeather.icon + '.png">',
                '</div>',
                '<div class="temp-container">',
                '<p class="temp-max">' + dayWeather.max + '°C</p>',
                '<p class="temp-min">' + dayWeather.min + '°C</p>',
                '</div>',
                '</div>',
                '<p class="humidity">Humidity: ' + dayWeather.humidity +'%</p>',
                '<p class="cloudiness">Cloudiness: ' + dayWeather.cloudiness + '%</p>',
                '<p class="wind">Wind: ' + dayWeather.windSpeed + ' mps</p>',
                '</div>'
            ].join('\n');
            _config.weatherContainer.append(html);
        }
    }

    return {
        init: init
    };
}());


$(document).ready(function () {
    TabNavigationHandler.init();
    WeatherForecastHandler.init();
});