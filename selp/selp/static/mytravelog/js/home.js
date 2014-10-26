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

$(document).ready(function () {
    scrollToPopularCities();
});