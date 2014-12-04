from django.db import models


class City(models.Model):
    name = models.CharField(max_length=128, null=False, unique=True)
    url_name = models.CharField(max_length=128, null=False)
    country_name = models.CharField(max_length=128, null=False)
    country_url_name = models.CharField(max_length=128, null=False)
    tourist_count = models.IntegerField(max_length=128, null=False)
    tourist_growth = models.DecimalField(max_digits=4, decimal_places=1, null=False)
    description = models.CharField(max_length=2500, null=False)
    rank = models.IntegerField(max_length=10, null=False, default=-1)

    def __unicode__(self):
        return self.name