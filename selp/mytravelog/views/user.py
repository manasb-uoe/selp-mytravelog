from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from mytravelog.models.album import Album
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


def sign_up(request):
    """
    Renders the sign up template. Creates a new user and user profile using the POST data provided.
    It first validates all the provided data. If no error message is returned by the validation
    function, then the user and user profile are created successfully and user is signed in. Else,
     the sign up template is rendered with the error message. Also, every time an error occurs,
     the previous data input by the user is also used while rendering the template (except password).
    """
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect('/mytravelog/user/' + user.username + '/')
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
            error = validate_sign_up_form(first_name, last_name, email, username, password, profile_picture, cover_picture)
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
                if profile_picture is not None:
                    new_user_profile.profile_picture = profile_picture
                if cover_picture is not None:
                    new_user_profile.cover_picture = cover_picture
                new_user_profile.user = new_user
                new_user_profile.save()

                # now, sign in the user
                new_user_to_be_signed_in = authenticate(username=username, password=password)
                login(request, new_user_to_be_signed_in)
                return HttpResponseRedirect('/mytravelog/user/' + new_user.username + '/')
            else:
                data_dict['error'] = error
                data_dict['previous_post_data'] = post_data
        return render(request, 'mytravelog/sign_up.html', data_dict)


def sign_in(request):
    """
    Renders the sign in template. Uses the POST data provided to sign in
    the user. If any incorrect details are provided, then the sign in template
    is rendered using an error message. Once the sign in is successful, user is
    navigated to their user page.
    """
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect('/mytravelog/user/' + user.username + '/')
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
                        return HttpResponseRedirect('/mytravelog/user/' + user.username + '/')
                    else:
                        data_dict['error'] = "Your account is disabled"
                else:
                    data_dict['error'] = "Incorrect username or password"

        return render(request, 'mytravelog/sign_in.html', data_dict)


def sign_out(request):
    """
    Signs out an authenticated user, and redirects them to
    the home page. If the user is already signed out, they are
    redirected to the sign in page.
    """
    user = request.user
    if user.is_authenticated():
        logout(request)
        return HttpResponseRedirect('/mytravelog/')
    else:
        return HttpResponseRedirect('/mytravelog/sign_in')


def show_user(request, username):
    """
    Renders the user_main template using the data of the user with the
    provided username.
    """
    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # get requested user and user profile
    requested_user = get_object_or_404(User, username=username)
    requested_user_profile = UserProfile.objects.get(user=requested_user)

    # get user albums and attach duration to each album
    requested_user_albums = Album.objects.get_user_albums_with_duration(requested_user_profile)

    # get user logs along with pictures, likes and comments for each log
    requested_user_logs = Log.objects.attach_additional_info_to_logs(Log.objects.get_user_logs(requested_user_profile),
                                                                     current_user_profile)

    # get user followers and following
    requested_user_followers = Follower.objects.get_requested_user_followers(requested_user_profile,
                                                                             current_user_profile)
    requested_user_following = Follower.objects.get_requested_user_following(requested_user_profile,
                                                                             current_user_profile)

    # check if requested user can be followed by current user
    # if yes, then check if requested user is being followed by current user
    can_follow = False
    is_followed = False
    if current_user != requested_user and current_user_profile is not None:
        can_follow = True
        is_followed = Follower.objects.is_requested_user_followed_by_current_user(requested_user_profile,
                                                                                  current_user_profile)

    # check if current user can edit profile
    can_edit_profile = False
    if current_user == requested_user:
        can_edit_profile = True

    data_dict = {
        'requested_user': requested_user,
        'requested_user_profile': requested_user_profile,
        'current_user_profile': current_user_profile,
        'requested_user_albums': requested_user_albums,
        'requested_user_logs': requested_user_logs,
        'requested_user_followers': requested_user_followers,
        'requested_user_following': requested_user_following,
        'can_follow': can_follow,
        'is_followed': is_followed,
        'can_edit_profile': can_edit_profile
    }
    return render(request, 'mytravelog/user_main.html', data_dict)


# ----------------------Helper functions------------------------

def validate_sign_up_form(first_name, last_name, email, username, password, profile_picture, cover_picture):
    """
    Validates the user data provided.
    :param first_name: first name of the user
    :param last_name: last name of the user
    :param email: email address of the user
    :param username: username of the user
    :param password: password of the user
    :param profile_picture: profile picture file of the user
    :param cover_picture: cover picture file of the user
    :return: an error message if any error occurs, else, None is returned
    """
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
    if profile_picture is not None:
        if profile_picture._size > 2048*1024:
            return "Max image size allowed is 2 mb"
    if cover_picture is not None:
        if cover_picture._size > 2048*1024:
            return "Max image size allowed is 2 mb"
    return None





