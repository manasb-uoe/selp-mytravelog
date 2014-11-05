/**
 * Created by Manas on 11/1/2014.
 */

//--------------------Base------------------------

function handleTabNavigation() {
    // navigate to logs if no hash found
    if (window.location.hash == '') {
        window.location.href = window.location.href + '#logs'
    }
    navigateToActiveTab();

    // navigate to active tab every time the hash changes
    $(window).on('hashchange', function () {
        navigateToActiveTab();
    });
}

function navigateToActiveTab() {
    var hash = window.location.hash;

    // only mark selected tab as active
    var activeTab = $('a[href="' + hash +'"]');
    activeTab.siblings().removeClass('tab-active');
    activeTab.addClass('tab-active');

    // only show active tab content
    var activeContent = $('.' + hash.substr(1) + '-content');
    activeContent.show();
    activeContent.siblings().hide();
}

//--------------------Albums------------------------

function handleAlbums() {
    var AddOrEditAlbumSelectors = {
        form: $('#add-or-edit-album-modal-form'),
        errorContainer: $('#add-or-edit-album-modal-error-container'),
        modalTitle: $('#add-or-edit-album-modal-title'),
        inputName: $('#add-or-edit-album-modal-name-input'),
        inputStartDate: $('#add-or-edit-album-modal-start-date-input'),
        inputEndDate: $('#add-or-edit-album-modal-end-date-input'),
        submitButton: $('#add-or-edit-album-modal-submit-button'),
        modal: $('#add-or-edit-album-modal')
    };

    $('#add-new-album-button').click(function () {
        showAddOrEditAlbumModal(AddOrEditAlbumSelectors, 'Add new album', '', '', '', 'Add', '/mytravelog/album/create/');
    });

    $('.album-dropdown-item-edit').click(function () {
        //get all data about the selected album
        var album = $(this).parents('.album');
        var id = album.attr('data-id');
        var name = album.children('.name').text();
        var startDate = album.attr('data-start-date');
        var endDate = album.attr('data-end-date');

        showAddOrEditAlbumModal(AddOrEditAlbumSelectors, 'Edit album', name, startDate, endDate, 'Save', '/mytravelog/album/update/' + id + '/');
    });

    var deleteAlbumSelectors = {
        albumName:  $('#delete-album-modal-album-name'),
        submitButton: $('#delete-album-modal-submit-button'),
        errorContainer: $('#delete-album-modal-error-container'),
        modal: $('#delete-album-modal')
    };

    $('.album-dropdown-item-delete').click(function () {
        //get all data about the selected album
        var album = $(this).parents('.album');
        var id = album.attr('data-id');
        var name = album.children('.name').text();
        showDeleteAlbumModal(deleteAlbumSelectors, id, name);
    });
}

function showAddOrEditAlbumModal(selectors, modalTitle, name, startDate, endDate, submitButtonText, action) {
    selectors.errorContainer.hide();
    selectors.errorContainer.empty();
    selectors.modalTitle.text(modalTitle);
    selectors.inputName.val(name);
    selectors.inputStartDate.val(startDate);
    selectors.inputEndDate.val(endDate);
    selectors.submitButton.text(submitButtonText);
    selectors.form.attr('action', action);
    selectors.modal.modal();

    selectors.form.unbind().submit(function (event) {
        event.preventDefault();
        submitAddOrEditAlbumForm($(this), selectors.form.attr('action'), selectors.errorContainer);
    });
}

function submitAddOrEditAlbumForm (form, url, errorContainer) {
    //clear and hide existing errors
    errorContainer.empty();
    errorContainer.hide();

    //get form data
    var formData = new FormData(form[0]);                  //get reference of the form DOM element
    formData.append('csrfmiddlewaretoken', csrf_token);    //token declared in user base template

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: formData,
        success: function (response) {
            var redirect_to = response['redirect_to'];
            var error_message = response['error'];
            if (redirect_to != null) {
                window.location.href = redirect_to;
            }
            else if (error_message != null) {
                errorContainer.append('<strong>Error! </strong>' + error_message);
                errorContainer.show();
            }
            else {
                window.location.reload();
            }
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}

function showDeleteAlbumModal(selectors, id, name) {
    selectors.albumName.text(name);
    selectors.modal.modal();

    selectors.submitButton.unbind().click(function () {
        submitDeleteAlbumRequest(selectors.errorContainer, id);
    });
}

function submitDeleteAlbumRequest(errorContainer, id) {
    //clear and hide existing errors
    errorContainer.empty();
    errorContainer.hide();

    $.ajax({
        url: '/mytravelog/album/delete/' + id + '/',
        type: "POST",
        dataType: "json",
        data: {
            album_id: id,
            csrfmiddlewaretoken: csrf_token
        },
        success: function (response) {
            var redirect_to = response['redirect_to'];
            var error_message = response['error'];
            if (redirect_to != null) {
                window.location.href = redirect_to;
            }
            else if (error_message != null) {
                errorContainer.append('<strong>Error! </strong>' + error_message);
                errorContainer.show();
            }
            else {
                window.location.reload();
            }
        }
    });
}


//--------------------Logs------------------------

function handleLogs() {
    var addLogSelectors= {
        form: $('#add-log-modal-form'),
        errorContainer: $('#add-log-modal-error-container'),
        inputLocation: $('#add-log-modal-location-input'),
        inputAlbum: $('#add-log-modal-album-input'),
        inputDescription: $('#add-log-modal-description-input'),
        submitButton: $('#add-log-modal-submit-button'),
        imageDropzone: $('#add-log-modal-image-dropzone'),
        modal: $('#add-log-modal')
    };

    $('#add-new-log-button').click(function () {
        showAddLogModal(addLogSelectors);
    });
}

function showAddLogModal(selectors) {
    selectors.errorContainer.hide();
    selectors.errorContainer.empty();
    selectors.inputAlbum.find('option[value="None"]').attr('selected', true);
    selectors.inputDescription.val('');
    selectors.modal.modal();

    selectors.form.unbind().submit(function (event) {
        event.preventDefault();
        submitAddLogForm(selectors.form, selectors.errorContainer, '/mytravelog/log/create/');
    });
}

function submitAddLogForm(form, errorContainer, url) {
    //clear and hide existing errors
    errorContainer.empty();
    errorContainer.hide();

    //get form data
    var formData = new FormData(form[0]);                  //get reference of the form DOM element
    formData.append('csrfmiddlewaretoken', csrf_token);    //token declared in user base template

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: formData,
        success: function (response) {
            var redirect_to = response['redirect_to'];
            var error_message = response['error'];
            if (redirect_to != null) {
                window.location.href = redirect_to;
            }
            else if (error_message != null) {
                errorContainer.append('<strong>Error! </strong>' + error_message);
                errorContainer.show();
            }
            else {
                window.location.reload();
            }
        },
        //Options to tell JQuery not to process data or worry about content-type
        cache: false,
        contentType: false,
        processData: false
    });
}


//--------------------Function calls go here------------------------

$(document).ready(function () {
    handleTabNavigation();
    handleAlbums();
    handleLogs();
});