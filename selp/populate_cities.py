from mytravelog.models.user_profile import UserProfile

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
                            country_url_name=city.country_url_name,
                            tourist_count=city.tourist_count,
                            tourist_growth=city.tourist_growth,
                            description=city.info)

    # order all cities by tourist count and rank them one by one
    cities = City.objects.order_by('-tourist_count')
    rank = 1
    for city in cities:
        city.rank = rank
        city.save()
        rank += 1

    # add edinburgh manually using the add_new_city helper function from City module
    City.add_new_city(name='Edinburgh',
                      country_name='UK',
                      tourist_count=15000000,
                      tourist_growth=2.6,
                      description='Edinburgh is the capital city of Scotland, situated in Lothian on the southern shore of the Firth of Forth. It is the second most populous city in Scotland and the seventh most populous in the United Kingdom.[4] The population in 2013 was 487,500.[1] Edinburgh lies at the heart of a Larger urban zone with a population of 778,000.[5]Edinburgh has been recognised as the capital of Scotland since at least the 15th century (after Scone, Perth, Roxburgh, and Stirling, respectively) but political power moved south to London after the Union of the Crowns in 1603 and the Union of Parliaments in 1707. After nearly three centuries of unitary government, a measure of self-government returned in the shape of the devolved Scottish Parliament, which officially opened in Edinburgh in 1999. The city is also the annual venue of the General Assembly of the Church of Scotland and home to many national institutions such as the National Museum of Scotland, the National Library of Scotland and the Scottish National Gallery. Edinburgh\'s relatively buoyant economy, traditionally centred on banking and insurance but now encompassing a wide range of businesses, makes it the biggest financial centre in the UK after London.[6] Many Scottish companies have established their head offices in the city.')

    print "End of city population script."
