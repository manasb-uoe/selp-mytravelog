/**
 * Created by Manas on 11/1/2014.
 */

function handleTabNavigation() {
    var urlSegments = $(location).attr('href').split('/');
    var currentPage = urlSegments[urlSegments.length - 2];
    var activeTab = $('a[href$="' + currentPage +'/"]');
    activeTab.addClass('tab-active');
}

function handleAddAlbumPopup() {
    $('.button-add-album').click(function () {
        $('#add-album-modal').modal();
    });

    $('#add-album-form').submit(function (event) {
        event.preventDefault();
        submitFormAjax($(this), "/mytravelog/album/create/", $('#error-container-album-modal'));
    });
}

function submitFormAjax (form, url, error_container) {
    //clear and hide all existing errors
    error_container.hide();
    error_container.empty();

    //get form data
    var form_data = new FormData(form[0]);                  //get reference of the form DOM element
    form_data.append('csrfmiddlewaretoken', csrf_token);    //token declared in user base template

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: form_data,
        success: function (response) {
            var redirect_to = response['redirect_to'];
            var error_message = response['error'];
            if (redirect_to != null) {
                window.location.href = redirect_to;
            }
            else {
                error_container.append('<strong>Error! </strong>' + error_message);
                error_container.show();
            }
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

$(document).ready(function () {
    handleTabNavigation();
    handleAddAlbumPopup();
});