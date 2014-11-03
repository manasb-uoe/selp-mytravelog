/**
 * Created by Manas on 11/1/2014.
 */

//--------------------Base------------------------

function handleTabNavigation() {
    var urlSegments = $(location).attr('href').split('/');
    var currentPage = urlSegments[urlSegments.length - 2];
    var activeTab = $('a[href$="' + currentPage +'/"]');
    activeTab.addClass('tab-active');
}


//--------------------Albums------------------------

function handleAlbums() {
    var selectors = {
        form: $('#add-or-edit-album-modal-form'),
        errorContainer: $('#add-or-edit-album-modal-error-container'),
        modalTitle: $('#add-or-edit-album-modal-title'),
        inputName: $('#add-or-edit-album-modal-name-input'),
        inputStartDate: $('#add-or-edit-album-modal-start-date-input'),
        inputEndDate: $('#add-or-edit-album-modal-end-date-input'),
        submitButton: $('#add-or-edit-album-modal-submit-button'),
        modal: $('#add-or-edit-album-modal')
    };

    $('.button-add-album').click(function () {
        showAddOrEditAlbumModal(selectors, 'Add new album', '', '', '', 'Add', '/mytravelog/album/create/');
    });

    $('.album-dropdown-item-edit').click(function () {
        //get all data about the selected album
        var album = $(this).parents('.album');
        var id = album.attr('data-id');
        var name = album.children('.name').text();
        var startDate = album.attr('data-start-date');
        var endDate = album.attr('data-end-date');

        showAddOrEditAlbumModal(selectors, 'Edit album', name, startDate, endDate, 'Save', '/mytravelog/album/update/' + id + '/');
    });

    selectors.form.submit(function (event) {
        event.preventDefault();
        submitAddOrEditAlbumForm($(this), selectors.form.attr('action'), selectors.errorContainer);
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
}

function submitAddOrEditAlbumForm (form, url, errorContainer) {
    //clear existing errors
    errorContainer.empty();

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
            else {
                errorContainer.append('<strong>Error! </strong>' + error_message);
                errorContainer.show();
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
});