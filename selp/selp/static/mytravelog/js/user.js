/**
 * Created by Manas on 11/1/2014.
 */

//--------------------Base------------------------

var TabNavigationHandler = (function () {

    var _config = {
        addNewLogButton: $('#add-new-log-button'),
        addNewAlbumButton: $('#add-new-album-button')
    };

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
        if (hash == '#logs') {
            _config.addNewAlbumButton.hide();
            _config.addNewLogButton.show();
        }
        else if (hash == '#albums') {
            _config.addNewAlbumButton.show();
            _config.addNewLogButton.hide();
        }
        else {
            _config.addNewAlbumButton.hide();
            _config.addNewLogButton.hide();
        }
    }

    function init() {
        // navigate to logs if no hash found
        if (window.location.hash == '') {
            window.location.href = window.location.href + '#logs'
        }
        _navigateToActiveTab();

        // navigate to active tab every time the hash changes
        $(window).on('hashchange', function () {
            _navigateToActiveTab();
        });
    }

    return {
        init:init
    };

}());


//--------------------Albums------------------------

function handleAlbums() {
    AddOrEditAlbumModal.init();
    DeleteAlbumModal.init();
}

var AddOrEditAlbumModal = (function() {

    var _config = {
        form: $('#add-or-edit-album-modal-form'),
        errorContainer: $('#add-or-edit-album-modal-error-container'),
        modalTitle: $('#add-or-edit-album-modal-title'),
        inputName: $('#add-or-edit-album-modal-name-input'),
        inputStartDate: $('#add-or-edit-album-modal-start-date-input'),
        inputEndDate: $('#add-or-edit-album-modal-end-date-input'),
        submitButton: $('#add-or-edit-album-modal-submit-button'),
        modal: $('#add-or-edit-album-modal'),
        dropdownItemEdit: $('.album-dropdown-item-edit'),
        addNewAlbumButton: $('#add-new-album-button'),
        submitUrl: ''
    };

    function _bindUIActions() {
        _config.addNewAlbumButton.click(function () {
            _showModal('Add new album', '', '', '', 'Add');
            _config.submitUrl = '/mytravelog/album/create/';
        });
        _config.dropdownItemEdit.click(function () {
            //get all data about the selected album
            var album = $(this).parents('.album');
            var id = album.attr('data-id');
            var name = album.children('.name').text();
            var startDate = album.attr('data-start-date');
            var endDate = album.attr('data-end-date');

            _showModal('Edit album', name, startDate, endDate, 'Save');
            _config.submitUrl = '/mytravelog/album/update/' + id + '/'
        });
        _config.form.submit(function (event) {
            event.preventDefault();
            submitForm($(this), _config.errorContainer, _config.submitUrl);
        });
    }

    function _showModal(modalTitle, name, startDate, endDate, submitButtonText) {
        _config.errorContainer.hide();
        _config.errorContainer.empty();
        _config.modalTitle.text(modalTitle);
        _config.inputName.val(name);
        _config.inputStartDate.val(startDate);
        _config.inputEndDate.val(endDate);
        _config.submitButton.text(submitButtonText);
        _config.modal.modal();
    }

    function init() {
        _bindUIActions();
    }

    return {
        init: init
    };
}());

var DeleteAlbumModal = (function () {

    var _config = {
        albumName:  $('#delete-album-modal-album-name'),
        albumCreatedAt: $('#delete-album-modal-created-at'),
        submitButton: $('#delete-album-modal-submit-button'),
        errorContainer: $('#delete-album-modal-error-container'),
        modal: $('#delete-album-modal'),
        dropdownItemDelete: $('.album-dropdown-item-delete'),
        submitUrl: ''
    };

    function _bindUIActions() {
        _config.dropdownItemDelete.click(function () {
            //get required data about the selected album
            var album = $(this).parents('.album');
            var id = album.attr('data-id');
            var name = album.children('.name').text();
            var createdAt = album.attr('data-created-at');

            _showModal(name, createdAt);
            _config.submitUrl = '/mytravelog/album/delete/' + id + '/';
        });
        _config.submitButton.click(function () {
            submitSimpleRequest(_config.errorContainer, _config.submitUrl);
        });
    }

    function _showModal(name, createdAt) {
        _config.albumName.text(name);
        _config.albumCreatedAt.text(createdAt);
        _config.modal.modal();
    }

    function init() {
        _bindUIActions();
    }

    return {
        init:init
    };
}());


//--------------------Logs------------------------

function handleLogs() {
    AddLogModal.init();
    DeleteLogModal.init();
    LogPicturesViewer.init();
    EditLogModal.init();
    LikeHandler.init();
    CommentHandler.init();
}

var AddLogModal = (function () {

    var _config = {
        form: $('#add-log-modal-form'),
        errorContainer: $('#add-log-modal-error-container'),
        mapContainer: $('#add-log-modal-map-container'),
        inputLocation: $('#add-log-modal-location-input'),
        inputLatitude: $('#add-log-modal-latitude-input'),
        inputLongitude: $('#add-log-modal-longitude-input'),
        inputAlbum: $('#add-log-modal-album-input'),
        inputDescription: $('#add-log-modal-description-input'),
        imagesContainer: $('#add-log-modal-images-container'),
        submitButton: $('#add-log-modal-submit-button'),
        moreImagesButton: $('#add-log-modal-more-images-button'),
        modal: $('#add-log-modal'),
        addNewLogButton: $('#add-new-log-button'),
        additionalImageCounter: 0
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.addNewLogButton.click(function () {
            _showModal();
        });
        // if multiple files are submitted with the same name, only the last file is received on the server side
        // to solve this, input name is changed based on a counter
        _config.moreImagesButton.click(function () {
            _config.additionalImageCounter++;
            _config.imagesContainer.append('<input class="form-control form-input" id="add-log-modal-image-input" name="log_picture_' + _config.additionalImageCounter + '" type="file">');
        });
        _config.form.submit(function (event) {
            event.preventDefault();
            submitForm($(this), _config.errorContainer, '/mytravelog/log/create/');
        });
    }

    function _showModal() {
        _config.errorContainer.hide();
        _config.errorContainer.empty();
        _config.inputAlbum.find('option[value="None"]').attr('selected', true);
        _config.inputDescription.val('');
        _config.imagesContainer.empty().append('<input class="form-control form-input" id="add-log-modal-image-input" name="log_picture_1" type="file">');
        _config.additionalImageCounter = 1;
        _config.modal.modal();

        //show current location on map and location input field
        setTimeout(_showCurrentPosition, 1000);
    }

    function _showCurrentPosition() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(_showCurrentPositionSuccessCallback, _showCurrentPositionFailureCallback);
        }
        else {
            console.log("Geolocation is not supported by this browser");
        }
    }

    function _showCurrentPositionSuccessCallback(position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var latlng = new google.maps.LatLng(lat, lng);

        //fill latitude and longitude form input fields
        _config.inputLatitude.val(lat);
        _config.inputLongitude.val(lng);

        //show current location on map
        var options = {
            zoom: 15,
            center: latlng,
            mapTypeControl: false,
            navigationControlOptions: {
                style: google.maps.NavigationControlStyle.SMALL
            },
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        var map = new google.maps.Map(_config.mapContainer[0], options);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            title:"You are here!"
        });
        marker.setMap(map);

        //reverse geocode latlng and then show current city and country in the input element provided
        _reverseGeocode(latlng);
    }

    function _showCurrentPositionFailureCallback(error) {
        var error_message = null;
        switch(error.code) {
            case error.PERMISSION_DENIED:
                error_message = "User denied the request for Geolocation.";
                break;
            case error.POSITION_UNAVAILABLE:
                error_message = "Location information is unavailable.";
                break;
            case error.TIMEOUT:
                error_message = "The request to get user location timed out.";
                break;
        }
        console.log(error_message);
    }

    function _reverseGeocode(latlng) {
        var geocoder = new google.maps.Geocoder();
        geocoder.geocode({'latLng': latlng}, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var city = null;
                    var country = null;
                    for (var i=0; i<results[0].address_components.length; i++) {
                        for (var b=0;b<results[0].address_components[i].types.length;b++) {
                            if (results[0].address_components[i].types[b] == "locality") {
                                city = results[0].address_components[i];
                            }
                            if (results[0].address_components[i].types[b] == "country") {
                                country = results[0].address_components[i];
                            }
                        }
                    }
                    if (city && country) {
                        _config.inputLocation.val(city.long_name + ", " + country.long_name);
                    }
                    else {
                        _config.inputLocation.val("Location not found");
                    }
                }
                else {
                    console.log("location not found");
                }
            }
            else {
                console.log("Geocoder failed due to: " + status);
            }
        });
    }

    return {
        init:init
    };
}());

var LogPicturesViewer = (function () {

    var _config = {
        logPicture: $('.log-picture'),
        modal: $('#log-picture-modal'),
        modalPictureContainer: $('#log-picture-modal-picture'),
        modalPreviousButton: $('#log-picture-modal-previous-button'),
        modalNextButton: $('#log-picture-modal-next-button'),
        modalIndex: $('#log-picture-modal-index'),
        currentIndex: 0,
        totalPictures: 0,
        urls: []
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.logPicture.click(function () {
            _config.logPicture = $(this);
            _getCurrentIndexAndUrls();
            _config.modal.modal();
        });
        _config.modal.on('shown.bs.modal', function(){
            _showCurrentPicture();
        });
        _config.modal.on('hidden.bs.modal', function(){
            _config.modalPictureContainer.html('');
        });
        _config.modalNextButton.click(function () {
            _config.currentIndex++;
            _showCurrentPicture();
        });
        _config.modalPreviousButton.click(function () {
            _config.currentIndex--;
            _showCurrentPicture();
        });
    }

    function _showCurrentPicture() {
        var img = '<div id="log-picture-modal-picture" style="background-image: url(\'' + _config.urls[_config.currentIndex] +'\')"/>';
        _config.modalPictureContainer.html(img);

        //set modal index
        _config.modalIndex.text(_config.currentIndex+1 + ' of ' + _config.totalPictures);

        // hide/show previous and next buttons depending on the index
        if (_config.currentIndex == _config.totalPictures-1) {
            _config.modalNextButton.css('visibility', 'hidden');
        }
        else {
            _config.modalNextButton.css('visibility', 'visible');
        }
        if (_config.currentIndex == 0) {
            _config.modalPreviousButton.css('visibility', 'hidden');
        }
        else {
            _config.modalPreviousButton.css('visibility', 'visible');
        }
    }

    function _getCurrentIndexAndUrls() {
        _config.urls = [];
        var logPicturesContainer = _config.logPicture.closest('.log-pictures-container');
        var logPictures = logPicturesContainer.find('.log-picture');
        logPictures.each(function () {
            _config.urls.push($(this).attr('data-url'));
        });
        _config.totalPictures = logPictures.length;

        //get index of selected picture
        var currentUrl = _config.logPicture.attr('data-url');
        for (var i=0; i<_config.totalPictures; i++) {
            if (_config.urls[i] == currentUrl) {
                _config.currentIndex = i;
            }
        }
    }

    return {
        init: init
    };
})();

var DeleteLogModal = (function () {
    var _config = {
        logLocation: $('#delete-log-modal-location'),
        logCreatedAt: $('#delete-log-modal-created-at'),
        submitButton: $('#delete-log-modal-submit-button'),
        errorContainer: $('#delete-log-modal-error-container'),
        dropdownItemDelete: $('.log-dropdown-item-delete'),
        modal: $('#delete-log-modal'),
        submitUrl: ''
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.dropdownItemDelete.click(function () {
            //get required data about the selected log
            var log = $(this).closest('.log');
            var id = log.attr('data-id');
            var location = log.attr('data-location');
            var createdAt = log.attr('data-created-at');

            _showModal(location, createdAt);
            _config.submitUrl = '/mytravelog/log/delete/' + id + '/';
        });
        _config.submitButton.click(function () {
            submitSimpleRequest(_config.errorContainer, _config.submitUrl);
        });
    }

    function _showModal(location, createdAt) {
        _config.logLocation.text(location);
        _config.logCreatedAt.text(createdAt);
        _config.modal.modal();
    }

    return {
        init:init
    };
}());

var EditLogModal = (function () {

    var _config = {
        form: $('#edit-log-modal-form'),
        errorContainer: $('#edit-log-modal-error-container'),
        mapContainer: $('#edit-log-modal-map-container'),
        inputLocation: $('#edit-log-modal-location-input'),
        inputAlbum: $('#edit-log-modal-album-input'),
        inputDescription: $('#edit-log-modal-description-input'),
        imagesContainer: $('#edit-log-modal-images-container'),
        submitButton: $('#edit-log-modal-submit-button'),
        moreImagesButton: $('#edit-log-modal-more-images-button'),
        modal: $('#edit-log-modal'),
        dropdownItemEdit: $('.log-dropdown-item-edit'),
        additionalImageCounter: 0,
        previousImagesContainer: $('#edit-log-modal-previous-images-container'),
        inputPreviousImagesToDelete: $('#edit-log-modal-images-to-delete'),
        submitUrl: ''
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.dropdownItemEdit.click(function () {
            //get required data about the selected log
            var log = $(this).closest('.log');
            var id = log.attr('data-id');
            var location = log.attr('data-location');
            var latitude = log.attr('data-latitude');
            var longitude = log.attr('data-longitude');
            var albumName = log.attr('data-album-name');
            var description = log.attr('data-description');

            var previousImagesInfo = {};
            var logPicturesContainer = log.children('.log-pictures-container');
            var logPictures = logPicturesContainer.find('.log-picture');
            logPictures.each(function () {
                previousImagesInfo[$(this).attr('data-id')] = $(this).attr('data-url');
            });

            _showModal(location, latitude, longitude, albumName, description, previousImagesInfo);

            _config.submitUrl = '/mytravelog/log/edit/' + id + '/';
        });
        // if multiple files are submitted with the same name, only the last file is received on the server side
        // to solve this, input name is changed based on a counter
        _config.moreImagesButton.click(function () {
            _config.additionalImageCounter++;
            _config.imagesContainer.append('<input class="form-control form-input" id="edit-log-modal-image-input" name="log_picture_' + _config.additionalImageCounter + '" type="file">');
        });
        _config.form.submit(function (event) {
            event.preventDefault();
            submitForm($(this), _config.errorContainer, _config.submitUrl);
        });
        _config.previousImagesContainer.on('click', '.edit-log-modal-previous-image', function () {
            // append picture id for every image clicked by user
            // this id would be used by the server to delete the corresponding pictures
            _config.inputPreviousImagesToDelete.val(_config.inputPreviousImagesToDelete.val() + $(this).attr('data-id') + ", ");
            $(this).css('display', 'none');

            var remainingImagesCounter = 0;
            _config.previousImagesContainer.children().each(function () {
                if ($(this).css('display') != 'none') {
                    remainingImagesCounter++;
                }
            });
            if (remainingImagesCounter == 0) {
                _config.previousImagesContainer.append('<p class="edit-log-modal-no-previous-images-text">No more images remaining</p>');
            }
            console.log(remainingImagesCounter);
        });
    }

    function _showModal(location, latitude, longitude, albumName, description, previousImageInfo) {
        _config.errorContainer.hide();
        _config.errorContainer.empty();
        _config.inputLocation.val(location);
        _config.inputAlbum.find('option[value="' + albumName + '"]').attr('selected', true);
        _config.inputDescription.val(description);
        _config.imagesContainer.empty().append('<input class="form-control form-input" id="edit-log-modal-image-input" name="log_picture_1" type="file">');
        _config.additionalImageCounter = 1;
        _config.previousImagesContainer.empty();
        for (var key in previousImageInfo) {
            if (previousImageInfo.hasOwnProperty(key)) {
                var imageHtml = [
                        '<div class="edit-log-modal-previous-image" data-id="' + key + '" style="background-image: url(\'' + previousImageInfo[key] + '\')">',
                    '<div class="edit-log-modal-previous-image-mask">',
                    '<div class="edit-log-modal-previous-image-delete-button"></div>',
                    '</div>',
                    '</div>'].join('\n');
                _config.previousImagesContainer.append(imageHtml);
            }
        }
        _config.inputPreviousImagesToDelete.val('');
        _config.modal.modal();

        //show location on map and location input field
        setTimeout(function () {
            _showPositionOnMap(latitude, longitude)
        }, 1000);
    }

    function _showPositionOnMap(latitude, longitude) {
        var latlng = new google.maps.LatLng(latitude, longitude);

        //show current location on map
        var options = {
            zoom: 15,
            center: latlng,
            mapTypeControl: false,
            navigationControlOptions: {
                style: google.maps.NavigationControlStyle.SMALL
            },
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        var map = new google.maps.Map(_config.mapContainer[0], options);
        var marker = new google.maps.Marker({
            position: latlng,
            map: map,
            title:"You were here!"
        });
        marker.setMap(map);
    }

    return {
        init:init
    };

}());

var LikeHandler = (function () {

    var _config = {
        likeButton: $('.like-log-button'),
        likeButtonInActiveClass: 'like-log-button',
        likeButtonActiveClass: 'like-log-button-active',
        dataLogIdAttr: 'data-log-id',
        createLikeOperation: 'create_like',
        deleteLikeOperation: 'delete_like',
        createLikeBaseUrl: '/mytravelog/like/create/',
        deleteLikeBaseUrl: '/mytravelog/like/delete/',
        likeAndCommentContainerClass: '.like-and-comment-container',
        likeAndCommentCountContainerClass: '.like-and-comment-count-container',
        likerProfilePicturesClass: '.liker-profile-pictures',
        likeCountContainerClass: '.like-count-container',
        countClass: '.count',
        maxLikerProfilePicturesAllowed: 14
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.likeButton.click(function () {
            var logId = $(this).attr(_config.dataLogIdAttr);
            var className = $(this).attr('class');
            if (className == _config.likeButtonInActiveClass) {
                _sendPostRequest(logId, _config.createLikeOperation , $(this));
            }
            else {
                _sendPostRequest(logId, _config.deleteLikeOperation, $(this));
            }
        });
    }

    function _sendPostRequest(logId, operation, likeButton) {
        var url = null;
        if (operation == _config.createLikeOperation) {
            url = _config.createLikeBaseUrl + logId + '/';
        }
        else {
            url = _config.deleteLikeBaseUrl + logId + '/';
        }

        $.ajax({
            url: url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrf_token
            },
            success: function (response) {
                var redirectTo = response['redirect_to'];
                if (redirectTo != null) {
                    window.location.href = redirectTo;
                }
                else {
                    var username = response['username'];
                    var profilePictureUrl = response['profile_picture_url'];
                    _postSuccessCallback(username, profilePictureUrl, operation, likeButton);
                }
            }
        });
    }

    function _postSuccessCallback(username, profilePictureUrl, operation, likeButton) {
        var likeAndCommentContainer = likeButton.parent(_config.likeAndCommentContainerClass);
        var likeAndCommentCountContainer = likeAndCommentContainer.siblings(_config.likeAndCommentCountContainerClass);
        var likerProfilePicturesContainer = likeAndCommentCountContainer.children(_config.likerProfilePicturesClass);
        var likeCount = likeAndCommentCountContainer.children(_config.likeCountContainerClass).children(_config.countClass);
        var likeCountVal = parseInt(likeCount.text());

        if (operation == _config.createLikeOperation) {
            likeButton.addClass(_config.likeButtonActiveClass);
            // increment like count, preprend profile picture of liker and delete last picture if total pictures == max pictures allowed
            likeCount.text(likeCountVal + 1);
            var imageHtml = [
                    '<a href="' + "/mytravelog/user/" + username + '/" data-toggle="tooltip" title="' + username + '">',
                    '<div class="liker-profile-picture" style="background-image: url(\'' + profilePictureUrl + '\')"></div>',
                '</a>'
            ].join('\n');
            likerProfilePicturesContainer.prepend(imageHtml);
            if (likerProfilePicturesContainer.children().length > _config.maxLikerProfilePicturesAllowed) {
                likerProfilePicturesContainer.children().last().remove();
            }
        }
        else {
            likeButton.removeClass(_config.likeButtonActiveClass);
            //decrement like count and remove profile picture of disliker
            likeCount.text(likeCountVal - 1);
            var linkToRemove = "/mytravelog/user/" + username + '/';
            likerProfilePicturesContainer.children().each(function () {
                if ($(this).attr('href') == linkToRemove) {
                    $(this).remove();
                }
            });
        }
    }

    return {
        init:init
    };

}());

var CommentHandler = (function () {

    var _config = {
        inputComment: $('.comment-log-input'),
        createCommentBaseUrl: '/mytravelog/comment/create/',
        deleteCommentBaseUrl: '/mytravelog/comment/delete/',
        dataLogIdAttr: 'data-log-id',
        dataCommentIdAttr: 'data-comment-id',
        createCommentOperation: 'create_comment',
        deleteCommentOperation: 'delete_comment',
        commentContainerClass: '.comment-container',
        commentDeleteButtonClass: '.comment-delete-button',
        likeAndCommentContainerClass: '.like-and-comment-container',
        likeAndCommentCountContainerClass: '.like-and-comment-count-container',
        commentCountContainerClass: '.comment-count-container',
        countClass: '.count',
        commentClass: '.comment'
    };

    function init() {
        _bindUIActions();
    }

    function _bindUIActions() {
        _config.inputComment.keypress(function (event) {
            //detect enter keypress
            if (event.which == 13) {
                var logId = $(this).attr(_config.dataLogIdAttr);
                var body = $(this).val();
                _sendPostRequest(logId, body, _config.createCommentOperation, $(this));
            }
        });
        $(_config.commentContainerClass).on('click', _config.commentDeleteButtonClass, function () {
            var commentId = $(this).attr(_config.dataCommentIdAttr);
            _sendPostRequest(commentId, null, _config.deleteCommentOperation, $(this));
        });
    }

    function _sendPostRequest(id, body, operation, inputComment) {
        var url = null;
        if (operation == _config.createCommentOperation) {
            url = _config.createCommentBaseUrl + id + '/';
        }
        else {
            url = _config.deleteCommentBaseUrl + id + '/';
        }

        $.ajax({
            url: url,
            type: "POST",
            data: {
                csrfmiddlewaretoken: csrf_token,
                body: body
            },
            success: function (response) {
                var redirectTo = response['redirect_to'];
                var error_message = response['error'];
                if (redirectTo != null) {
                    window.location.href = redirectTo;
                }
                else if (error_message != null) {
                    window.alert(error_message);
                }
                else {
                    _postSuccessCallback(response, operation, inputComment);
                }
            }
        });
    }

    // if operation == create_comment, then selector is inputComment, else the selector is deleteButton
    function _postSuccessCallback(response, operation, selector) {
        selector.val("");
        var likeAndCommentContainer = null;
        var likeAndCommentCountContainer = null;
        var commentCount = null;
        var commentCountVal = 0;

        if (operation == _config.createCommentOperation) {
            likeAndCommentContainer = selector.parent(_config.likeAndCommentContainerClass);
            likeAndCommentCountContainer = likeAndCommentContainer.siblings(_config.likeAndCommentCountContainerClass);
            commentCount = likeAndCommentCountContainer.children(_config.commentCountContainerClass).children(_config.countClass);
            commentCountVal = parseInt(commentCount.text());
            var commentContainer = likeAndCommentContainer.children(_config.commentContainerClass);

            // increment comment count and add comment
            commentCount.text(commentCountVal + 1);
            var commentHtml = [
                '<div class="comment">',
                    '<a href="/mytravelog/user/' + response['username'] + '/">',
                    '<div class="comment-profile-picture" style="background-image: url(' + response['profile_picture_url'] + ')"></div>',
                '</a>',
                '<div class="comment-content">',
                '<div class="comment-header">',
                    '<a class="comment-full-name" href="/mytravelog/user/' + response['username'] + '/">' + response['full_name'] + '</a>',
                    '<a class="comment-username" href="/mytravelog/user/' + response['username'] + '/">' + response['username'] + '</a>',
                    '<p class="comment-timestamp">• ' + response['created_at'] + '</p>',
                '</div>',
                    '<p class="comment-body">' + response['body'] + '</p>',
                    '<p class="comment-delete-button" data-comment-id="' + response['comment_id'] + '">Delete</p>',
                '</div>',
                '</div>'
            ].join('\n');
            commentContainer.append(commentHtml);
        }
        else {
            likeAndCommentContainer = selector.parents(_config.likeAndCommentContainerClass);
            likeAndCommentCountContainer = likeAndCommentContainer.siblings(_config.likeAndCommentCountContainerClass);
            commentCount = likeAndCommentCountContainer.children(_config.commentCountContainerClass).children(_config.countClass);
            commentCountVal = parseInt(commentCount.text());

            //decrement comment count and delete comment
            commentCount.text(commentCountVal - 1);
            var commentToDelete = selector.closest(_config.commentClass);
            commentToDelete.remove();
        }
    }

    return {
        init:init
    };

}());

//--------------------Helper functions------------------------

function submitForm(form, errorContainer, url) {
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

function submitSimpleRequest(errorContainer, url) {
    //clear and hide existing errors
    errorContainer.empty();
    errorContainer.hide();

    $.ajax({
        url: url,
        type: "POST",
        dataType: "json",
        data: {
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


//--------------------Function calls go here------------------------

$(document).ready(function () {
    TabNavigationHandler.init();
    handleAlbums();
    handleLogs();
});