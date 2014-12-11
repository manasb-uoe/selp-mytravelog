from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render

from mytravelog.models.city import City
from mytravelog.models.follower import Follower
from mytravelog.models.user_profile import UserProfile


__author__ = 'Manas'


def search_for_cities_and_users(request):
    """
    Renders the search template using the results based on the query provided
    in the GET request (using the helper function get_search_results). If exactly
    1 city matches the query, the the user is redirected to its city page.
    Else, the search results are shown.
    """
    search_query = request.GET.get('query', None)
    if search_query is not None:
        # if query exactly matches a city, go directly to its city page
        # else, get all cities and users matching the query
        city = City.objects.filter(name__iexact=search_query)
        if len(city) == 1:
            return HttpResponseRedirect('/mytravelog/city/' + city[0].url_name + '/')
        else:
            results = get_search_results(search_query)
            cities = results['cities']
            user_profiles = results['user_profiles']
            # check if each user profile returned is being followed by current user
            user = request.user
            can_follow = False
            if user.is_authenticated():
                can_follow = True
                current_user_profile = UserProfile.objects.get(user=user)
                for user_profile in user_profiles:
                    user_profile.is_followed = Follower.objects.is_requested_user_followed_by_current_user(user_profile,
                                                                                                           current_user_profile)

            results_count = len(cities) + len(user_profiles)
            data_dict = {'cities': cities,
                         'user_profiles': user_profiles,
                         'results_count': results_count,
                         'query': search_query,
                         'can_follow': can_follow}
            return render(request, 'mytravelog/search.html', data_dict)
    else:
        raise Http404


# ---------Helper functions-----------

def get_search_results(query):
    """
    Queries the models based on the query provided.
    :param query: the search term
    :return: a dict containing the filtered cities and user profiles
    """
    cities = City.objects.filter(Q(name__startswith=query) |
                                 Q(country_name__startswith=query))
    user_profiles = UserProfile.objects.filter(Q(user__username__startswith=query) |
                                               Q(user__first_name__startswith=query) |
                                               Q(user__last_name__startswith=query))
    return {
        'cities': cities,
        'user_profiles': user_profiles
    }