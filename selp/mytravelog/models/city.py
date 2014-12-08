from re import sub
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

    @staticmethod
    def add_new_city(**kwargs):
        name = kwargs.get('name')
        url_name = sub(r'\s', '_', name)
        country_name = kwargs.get('country_name')
        country_url_name = sub('\s', '_', country_name)
        City.objects.create(name=name,
                            url_name=url_name,
                            country_name=country_name,
                            country_url_name=country_url_name,
                            tourist_count=kwargs.get('tourist_count'),
                            tourist_growth=kwargs.get('tourist_growth'),
                            description=kwargs.get('description'))

        # get all cities and update their ranks
        cities = City.objects.order_by('-tourist_count')
        rank = 1
        for city in cities:
            city.rank = rank
            city.save()
            rank += 1