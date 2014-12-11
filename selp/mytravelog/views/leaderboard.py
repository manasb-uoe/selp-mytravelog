from operator import attrgetter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import render
from mytravelog.models.city import City
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile
from update_user_ranks import update_user_ranks

__author__ = 'Manas'


def show_leaderboard(request, model):
    """
    Renders the leaderboard template using the results based
    on the model provided. The results are obtained using the
    helper function: get_results. Model can only take two values:
    'users' or 'cities'. The results are first paginated,
    and then only those results belonging to the requested page
    number are used while rendering the template.
    """
    get_data = request.GET
    page_num = get_data.get('page', 1)
    query = get_data.get('query', '')
    order_by = get_data['order_by'] if len(get_data.get('order_by', '')) > 0 else 'rank'
    order = get_data.get('order', 'asc')

    if model == 'users':
        # rank all users on every page load - this is only a temporary solution
        # in production, update_users_ranks script should be scheduled to run
        # every few hours/minutes
        update_user_ranks()

        # get all user profiles and sort them by increasing order of rank
        items = get_results(query, model, order_by, order)
    elif model == 'cities':
        # get all cities and sort them by increasing order of rank
        items = get_results(query, model, order_by, order)
    else:
        raise Http404
    # paginate leaderboard items
    paginator = Paginator(items, 30)
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
        'model': model,
        'query': query
    }
    return render(request, 'mytravelog/leaderboard.html', data_dict)


# ---------------Helper functions------------------

def get_results(query, model, order_by, order):
    """
    Returns filtered results based on the parameters provided.
    :param query: the search term
    :param model: tells the function which model to query on. Can only take two values: 'users' or 'cities'
    :param order_by: the field name by which the results should be sorted
    :param order: the order in which the results should be sorted. Can only take two values: 'asc' or 'desc'
    :return: List of cities or user profiles (depends on the model provided)
    """
    if model == 'users':
        results = UserProfile.objects.filter(
            Q(user__username__startswith=query) |
            Q(user__first_name__startswith=query) |
            Q(user__last_name__startswith=query))
        if order_by == 'first_name' or order_by == 'username':
            if order == 'asc':
                results = attach_log_and_follower_count(results.order_by('user__' + order_by))
            else:
                results = attach_log_and_follower_count(results.order_by('-user__' + order_by))
        else:
            if order == 'asc':
                results = sorted(attach_log_and_follower_count(results), key=attrgetter(order_by))
            else:
                results = sorted(attach_log_and_follower_count(results), key=attrgetter(order_by), reverse=True)
    else:
        results = City.objects.filter(
            Q(name__startswith=query) |
            Q(country_name__startswith=query))
        if order == 'asc':
            results = results.order_by(order_by)
        else:
            results = results.order_by('-' + order_by)
    return results


def attach_log_and_follower_count(results):
    """
    Attaches log and followe counts on each of the user profiles
    provided in the results list
    :param results: list of user profiles
    :return: list of user profiles, log_count and follower_count has been attached to each user profile
    """
    # get no. of logs and followers for each user_profile
    for user_profile in results:
        user_profile.log_count = Log.objects.filter(user_profile=user_profile).count()
        user_profile.follower_count = Follower.objects.get_follower_count(user_profile)
    return results