/**
 * Created by Manas on 11/1/2014.
 */

function handleTabNavigation() {
    var urlSegments = $(location).attr('href').split('/');
    var currentPage = urlSegments[urlSegments.length - 2];
    var activeTab = $('a[href$="' + currentPage +'/"]');
    activeTab.addClass('tab-active');
}

$(document).ready(function () {
    handleTabNavigation();
});