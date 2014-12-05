from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import Http404
from django.shortcuts import render
from mytravelog.models.city import City
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def show_leaderboard(request, model):
    items = None
    if model == 'users':
        # get all user profiles and sort them by increasing order of rank
        items = UserProfile.objects.order_by('rank')
        # get no. of logs and followers for each user_profile
        for user_profile in items:
            user_profile.log_count = Log.objects.filter(user_profile=user_profile).count()
            user_profile.follower_count = Follower.objects.filter(following_user_profile=user_profile).count()
    elif model == 'cities':
        # get all cities and sort them by increasing order of rank
        items = City.objects.order_by('rank')
    else:
        raise Http404
    # paginate leaderboard items
    paginator = Paginator(items, 30)
    page_num = request.GET.get('page')
    try:
        items = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    data_dict = {
        'requested_page_items': items,
        'requested_model': model
    }
    return render(request, 'mytravelog/leaderboard.html', data_dict)
