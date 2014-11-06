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
    var addOrEditAlbumSelectors = {
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
        showAddOrEditAlbumModal(addOrEditAlbumSelectors, 'Add new album', '', '', '', 'Add', '/mytravelog/album/create/');
    });

    $('.album-dropdown-item-edit').click(function () {
        //get all data about the selected album
        var album = $(this).parents('.album');
        var id = album.attr('data-id');
        var name = album.children('.name').text();
        var startDate = album.attr('data-start-date');
        var endDate = album.attr('data-end-date');

        showAddOrEditAlbumModal(addOrEditAlbumSelectors, 'Edit album', name, startDate, endDate, 'Save', '/mytravelog/album/update/' + id + '/');
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

function showAddOrEditAlbumModal(selectors, modalTitle, name, startDate, endDate, submitButtonText, url) {
    selectors.errorContainer.hide();
    selectors.errorContainer.empty();
    selectors.modalTitle.text(modalTitle);
    selectors.inputName.val(name);
    selectors.inputStartDate.val(startDate);
    selectors.inputEndDate.val(endDate);
    selectors.submitButton.text(submitButtonText);
    selectors.modal.modal();

    selectors.form.unbind().submit(function (event) {
        event.preventDefault();
        submitForm($(this), selectors.errorContainer, url);
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
        mapContainer: $('#add-log-modal-map-container'),
        inputLocation: $('#add-log-modal-location-input'),
        inputAlbum: $('#add-log-modal-album-input'),
        inputDescription: $('#add-log-modal-description-input'),
        imagesContainer: $('#add-log-modal-images-container'),
        submitButton: $('#add-log-modal-submit-button'),
        moreImagesButton: $('#add-log-modal-more-images-button'),
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
    selectors.imagesContainer.empty().append('<input class="form-control form-input" id="add-log-modal-image-input" name="log_picture_1" type="file">');
    selectors.modal.modal();

    // if multiple files are submitted with the same name, only the last file is received on the server side
    // to solve this, input name is changed based on a counter
    var imageCounter = 1;
    selectors.moreImagesButton.unbind().click(function () {
        imageCounter++;
        selectors.imagesContainer.append('<input class="form-control form-input" id="add-log-modal-image-input" name="log_picture_' + imageCounter + '" type="file">');
    });

    //show current location on map and location input field
    var locationDisplayer = new LocationDisplayer(selectors.mapContainer[0], selectors.inputLocation);
    setTimeout(locationDisplayer.showCurrentLocation, 1000);

    selectors.form.unbind().submit(function (event) {
        event.preventDefault();
        submitForm($(this), selectors.errorContainer, '/mytravelog/log/create/');
    });
}

// This class is used to show current location in the provided map container and input field
function LocationDisplayer(mapContainer, locationInput) {

    this.showCurrentLocation = function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(success, failure);
        }
        else {
            console.log("Geolocation is not supported by this browser");
        }
    };

    var success = function (position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var latlng = new google.maps.LatLng(lat, lng);

        //show current location on map
        if (mapContainer != null) {
            var options = {
                zoom: 15,
                center: latlng,
                mapTypeControl: false,
                navigationControlOptions: {
                    style: google.maps.NavigationControlStyle.SMALL
                },
                mapTypeId: google.maps.MapTypeId.ROADMAP
            };

            var map = new google.maps.Map(mapContainer, options);
            var marker = new google.maps.Marker({
                position: latlng,
                map: map,
                title:"You are here!"
            });
            marker.setMap(map);
        }

        //reverse geocode latlng and then show current city and country in the input element provided
        if (locationInput != null) {
            reverseGeocode(latlng, locationInput);
        }
    };

    var failure = function (error) {
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
    };

    var reverseGeocode = function (latlng, locationInput) {
        var currentLocation = null;
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
                        locationInput.val(city.long_name + ", " + country.long_name);
                    }
                    else {
                        locationInput.val("Location not found");
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
    };

    //sample api output for reference
//{
//   "results" : [
//      {
//         "address_components" : [
//            {
//               "long_name" : "Miami",
//               "short_name" : "Miami",
//               "types" : [ "locality", "political" ]
//            },
//            {
//               "long_name" : "Miami-Dade County",
//               "short_name" : "Miami-Dade County",
//               "types" : [ "administrative_area_level_2", "political" ]
//            },
//            {
//               "long_name" : "Florida",
//               "short_name" : "FL",
//               "types" : [ "administrative_area_level_1", "political" ]
//            },
//            {
//               "long_name" : "United States",
//               "short_name" : "US",
//               "types" : [ "country", "political" ]
//            }
//         ],
//         "formatted_address" : "Miami, FL, USA",
//         "geometry" : {
//            "bounds" : {
//               "northeast" : {
//                  "lat" : 25.8556059,
//                  "lng" : -80.14240029999999
//               },
//               "southwest" : {
//                  "lat" : 25.709042,
//                  "lng" : -80.31975989999999
//               }
//            },
//            "location" : {
//               "lat" : 25.7890972,
//               "lng" : -80.2040435
//            },
//            "location_type" : "APPROXIMATE",
//            "viewport" : {
//               "northeast" : {
//                  "lat" : 25.8556059,
//                  "lng" : -80.14240029999999
//               },
//               "southwest" : {
//                  "lat" : 25.709042,
//                  "lng" : -80.31975989999999
//               }
//            }
//         },
//         "types" : [ "locality", "political" ]
//      }
//   ],
//   "status" : "OK"
//}
}


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


//--------------------Function calls go here------------------------

$(document).ready(function () {
    handleTabNavigation();
    handleAlbums();
    handleLogs();
});