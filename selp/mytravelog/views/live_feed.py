from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from mytravelog.models.album import Album
from mytravelog.models.follower import Follower
from mytravelog.models.log import Log
from mytravelog.models.user_profile import UserProfile

__author__ = 'Manas'


def show_live_feed(request, feed_filter):
    """
    Renders the live_feed template based on the results queried
    using the provided fieed filter. feed_filter only takes two
    values: 'all' or 'following'. If 'all' is provided, then logs
    from all users are returned sorted in descending order of their
    scores. if 'following' is provided, then logs from only those
    users are returned, which are being followed by the current user.
    The results are first paginated, and then only those results
    belonging to the requested page number are used while rendering
    the template.
    """
    # get current user and user profile
    current_user = request.user
    current_user_profile = None
    if current_user.is_authenticated():
        current_user_profile = UserProfile.objects.get(user=current_user)

    # filter logs based on feed filter
    if feed_filter == 'all':
        # get all logs
        requested_logs = Log.objects.all()
    elif feed_filter == 'following':
        # check if user is authenticated
        if current_user_profile is not None:
            # only get logs of users followed by current user
            current_user_following = Follower.objects.get_requested_user_following(current_user_profile, None).values('following_user_profile')
            requested_logs = Log.objects.get_users_logs(current_user_following)
        else:
            return HttpResponseRedirect('/mytravelog/sign_in')
    else:
        raise Http404

    # sort logs by descending order of score
    requested_logs = score_and_sort_logs(requested_logs)

    # paginate the logs
    paginator = Paginator(requested_logs, 10)
    page_num = request.GET.get('page')
    try:
        requested_page_logs = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        requested_page_logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        requested_page_logs = paginator.page(paginator.num_pages)

    # attach additional info (likes, comments and pictures) to page logs
    requested_page_logs = Log.objects.attach_additional_info_to_logs(requested_page_logs, current_user_profile)

    # get all albums for the current user in order to populate the Albums drop-down list while
    # editing a log (EditLogModal)
    current_user_albums = Album.objects.filter(user_profile=current_user_profile)

    data_dict = {
        'current_user_profile': current_user_profile,
        'current_user_albums': current_user_albums,
        'requested_page_logs': requested_page_logs,
        'requested_filter': feed_filter
    }
    return render(request, 'mytravelog/live_feed.html', data_dict)


def score_and_sort_logs(logs):
    """
    Scores each log provided, sorts them, and then returns the sorted list.
    :param logs: a list of logs to be scored and sorted
    :return: a list of logs sorted by descending order of their scores
    """
    for log_to_score in logs:
        log_to_score.score = log_to_score.get_log_score()
        log_to_score.save()
    return sorted(logs, key=lambda x: x.score, reverse=True)