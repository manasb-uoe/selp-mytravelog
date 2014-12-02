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


$(document).ready(function () {
    TabNavigationHandler.init();
});