__author__ = 'Manas'

import os
import django

if __name__ == "__main__":
    # setup django environment
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selp.settings")

    from mytravelog.models.city import City
    from mytravelog.utils.city_parser.city_parser import deserialize, wikipedia
    django.setup()

    # first, delete all existing cities
    City.objects.all().delete()

    # now, deserialize and add all city data
    cities = deserialize(wikipedia)
    for city in cities:
        City.objects.create(name=city.name,
                            url_name=city.url_name,
                            country_name=city.country_name,
                            tourist_count=city.tourist_count,
                            tourist_growth=city.tourist_growth,
                            description = city.info)
    print "End of city population script."
