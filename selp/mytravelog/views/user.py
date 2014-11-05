from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from mytravelog.models.album import Album
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def sign_up(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/mytravelog/')
    else:
        data_dict = {}
        if request.method == "POST":
            post_data = request.POST
            file_data = request.FILES
            first_name = post_data.get('first_name', "")
            last_name = post_data.get('last_name', "")
            email = post_data.get('email', "")
            username = post_data.get('username', "")
            password = post_data.get('password', "")
            profile_picture = file_data.get('profile_picture', None)
            cover_picture = file_data.get('cover_picture', None)

            # validate user input
            error = validate_sign_up_form(first_name, last_name, email, username, password)
            if error is None:
                # create new user
                new_user = User()
                new_user.first_name = first_name
                new_user.last_name = last_name
                new_user.email = email
                new_user.username = username
                new_user.set_password(password)  # encrypt password
                new_user.save()

                # create new user profile
                new_user_profile = UserProfile()
                new_user_profile.city_count = 0
                new_user_profile.country_count = 0
                new_user_profile.log_count = 0
                new_user_profile.total_score = 0
                if profile_picture is not None:
                    new_user_profile.profile_picture = profile_picture
                if cover_picture is not None:
                    new_user_profile.cover_picture = cover_picture
                new_user_profile.user = new_user
                new_user_profile.save()

                # now, sign in the user
                new_user_to_be_signed_in = authenticate(username=username, password=password)
                login(request, new_user_to_be_signed_in)
                return HttpResponseRedirect('/mytravelog/')
            else:
                data_dict['error'] = error
                data_dict['previous_post_data'] = post_data
        return render(request, 'mytravelog/sign_up.html', data_dict)


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/mytravelog/')
    else:
        data_dict = {}
        if request.method == "POST":
            post_data = request.POST
            username = post_data.get('username', "")
            password = post_data.get('password', "")
            # validate user input
            if len(username) == 0:
                data_dict['error'] = "Username is required"
            elif len(password) == 0:
                data_dict['error'] = "Password is required"
            else:
                data_dict['previous_post_data'] = post_data
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        # now, sign in in the user
                        login(request, user)
                        return HttpResponseRedirect('/mytravelog/')
                    else:
                        data_dict['error'] = "Your account is disabled"
                else:
                    data_dict['error'] = "Incorrect username or password"

        return render(request, 'mytravelog/sign_in.html', data_dict)


def sign_out(request):
    if request.user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/mytravelog/')
    else:
        return HttpResponseRedirect('/mytravelog/sign_in')


def show_user(request, username):
    data_dict = get_permissions(username, request.user)

    # get user albums and attach duration to each album
    requested_user_albums = Album.objects.filter(user_profile=data_dict['requested_user_profile'])
    for album in requested_user_albums:
        duration = (album.end_date - album.start_date).days
        album.duration = duration
    data_dict['requested_user_albums'] = requested_user_albums

    return render(request, 'mytravelog/user.html', data_dict)


# ----------------------Helper functions------------------------

def validate_sign_up_form(first_name, last_name, email, username, password):
    if len(first_name) == 0:
        return "First name is required"
    if len(last_name) == 0:
        return "Last name is required"
    if len(email) == 0:
        return "Email is required"
    if "@" not in email:
        return "Email is missing the '@' symbol"
    if len(username) == 0:
        return "Username is required"
    if len(username) < 6:
        return "Username must be at least 6 characters long"
    if " " in username:
        return "Username cannot contain spaces"
    if len(password) == 0:
        return "Password is required"
    if len(password) < 6:
        return "Password must be at least 6 characters long"
    if len(User.objects.filter(username=username)) > 0:
        return "That username is not available"
    return None


def get_permissions(username, current_user):
    # get requested user and user profile
    requested_user = get_object_or_404(User, username=username)
    requested_user_profile = UserProfile.objects.get(user=requested_user)

    # get permissions
    authenticated_to_edit_profile = False
    if current_user.is_authenticated():
        if current_user.username == requested_user.username:
            authenticated_to_edit_profile = True

    # get current user profile only if authenticated
    current_user_profile = None
    if authenticated_to_edit_profile:
        current_user_profile = get_object_or_404(UserProfile, user=current_user)

    # load all the required data and permissions into a dict
    data_dict = {'requested_user': requested_user,
                 'requested_user_profile': requested_user_profile,
                 'authenticated_to_edit_profile': authenticated_to_edit_profile,
                 'current_user_profile': current_user_profile}

    return data_dict