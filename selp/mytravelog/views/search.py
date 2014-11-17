from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render
from mytravelog.models.city import City
from mytravelog.models.follower import Follower
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def search_for_cities_and_users(request):
    search_query = request.GET.get('query', None)
    if search_query is not None:
        # if query exactly matches a city, go directly to its city page
        # else, get all cities and users matching the query
        city = City.objects.filter(name__iexact=search_query)
        if len(city) == 1:
            return HttpResponseRedirect('/mytravelog/city/' + city[0].url_name + '/')
        else:
            cities = City.objects.filter(Q(name__startswith=search_query) |
                                         Q(country_name__startswith=search_query))
            user_profiles = UserProfile.objects.filter(Q(user__username__startswith=search_query) |
                                                       Q(user__first_name__startswith=search_query) |
                                                       Q(user__last_name__startswith=search_query))
            # check if each user profile returned is being followed by current user
            user = request.user
            authenticated_to_follow = False
            if user.is_authenticated():
                authenticated_to_follow = True
                current_user_profile = UserProfile.objects.get(user=user)
                for user_profile in user_profiles:
                    user_profile.followed = False
                    if len(Follower.objects.filter(follower_user_profile=current_user_profile, following_user_profile=user_profile)) > 0:
                        user_profile.followed = True

            results_count = len(cities) + len(user_profiles)
            data_dict = {'cities': cities,
                         'user_profiles': user_profiles,
                         'results_count': results_count,
                         'query': search_query,
                         'authenticated_to_follow': authenticated_to_follow}
            return render(request, 'mytravelog/search.html', data_dict)
    else:
        raise Http404

