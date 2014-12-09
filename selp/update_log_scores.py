import os
import django

__author__ = 'Manas'

if __name__ == "__main__":
    # setup django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selp.settings")

    from mytravelog.models.log import Log

    django.setup()

    # get all logs and score them
    all_logs = Log.objects.all()
    for log_to_score in all_logs:
        log_to_score.score = log_to_score.get_log_score()
        log_to_score.save()

    print "End of log scoring script."