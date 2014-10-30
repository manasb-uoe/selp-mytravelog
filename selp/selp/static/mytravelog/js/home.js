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

function getCityAutocompleteSuggestions() {
    var input_city_text = $('.input-city-text');
    var suggestions_container = $('.autocomplete-suggestions-container');
    input_city_text.keyup(function () {
        var search_term = input_city_text.val();
        if (search_term.length > 1) {
            $.ajax({
                url: "/mytravelog/city/autocomplete/?search_term=" + search_term,
                type: "get",
                dataType: "json",
                success: function(data) {
                    // clear suggestions container for populating it
                    suggestions_container.empty();
                    var counter = 1;
                    for (var key in data) {
                        if (data.hasOwnProperty(key)) {
                            if (counter % 2 == 0) {
                                suggestions_container.append('<div class="suggestion-light">' + data[key]['city'] + ", " + data[key]['country'] + '</div>');
                            }
                            else {
                                suggestions_container.append('<div class="suggestion-dark">' + data[key]['city'] + ", " + data[key]['country'] + '</div>');
                            }
                            counter++;
                        }
                    }
                }
            });
        }
        else {
            suggestions_container.empty();
        }
    });

    //handle clicks
    suggestions_container.on('click', '.suggestion-light, .suggestion-dark', function () {
        var search_term = $(this).text();
        var city_name = search_term.substring(0, search_term.indexOf(','));
        input_city_text.val(city_name);
        suggestions_container.empty();
        window.location.href = '/mytravelog/search/?query=' + city_name;
    });
}

$(document).ready(function () {
    scrollToPopularCities();
    getCityAutocompleteSuggestions();
});