/**
 * Created by Manas on 10/26/2014.
 */

function scrollToPopularCities() {
    $('.explore-popular-cities').click(function () {
        $('body, html').animate({
            scrollTop: $('.divider').offset().top - $('.navbar').height()
        }, 400);
    });
}

var CityAutocompleteSuggestionsHandler = (function () {

    var _config = {
        inputCityText: $('.input-city-text'),
        suggestionsContainer: $('.autocomplete-suggestions-container'),
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.inputCityText.keyup(function () {
            _populateSuggestionsContainer();
        });
        _config.suggestionsContainer.on('click', '.suggestion-light, .suggestion-dark', function () {
            _handleSuggestionClick($(this));
        });
    }

    function _populateSuggestionsContainer() {
        var search_term = _config.inputCityText.val();
        if (search_term.length > 1) {
            $.ajax({
                url: "/mytravelog/city/autocomplete/?search_term=" + search_term,
                type: "get",
                dataType: "json",
                success: function(data) {
                    // clear suggestions container for populating it
                    _config.suggestionsContainer.empty();
                    var counter = 1;
                    for (var key in data) {
                        if (data.hasOwnProperty(key)) {
                            if (counter % 2 == 0) {
                                _config.suggestionsContainer.append('<div class="suggestion suggestion-light">' + data[key]['city'] + ", " + data[key]['country'] + '</div>');
                            }
                            else {
                                _config.suggestionsContainer.append('<div class="suggestion suggestion-dark">' + data[key]['city'] + ", " + data[key]['country'] + '</div>');
                            }
                            counter++;
                        }
                    }
                }
            });
        }
        else {
            _config.suggestionsContainer.empty();
        }
    }

    function _handleSuggestionClick(suggestion) {
        var search_term = suggestion.text();
        var city_name = search_term.substring(0, search_term.indexOf(','));
        _config.inputCityText.val(city_name);
        _config.suggestionsContainer.empty();
        window.location.href = '/mytravelog/search/?query=' + city_name;
    }

    return {
        init: init
    };

}());

$(document).ready(function () {
    scrollToPopularCities();
    CityAutocompleteSuggestionsHandler.init();
});