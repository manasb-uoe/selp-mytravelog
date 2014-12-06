from mytravelog.views.city import add_new_city

__author__ = 'Manas'

city1_sample_data = {
    'name': 'city1',
    'country_name': 'country1',
    'tourist_count': 1,
    'tourist_growth': 2,
    'description': 'desc1'
}
city2_sample_data = {
    'name': 'city2',
    'country_name': 'country2',
    'tourist_count': 2,
    'tourist_growth': 2,
    'description': 'desc2'
}


def add_sample_city(city_sample_data):
    add_new_city(name=city_sample_data['name'],
                 country_name=city_sample_data['country_name'],
                 tourist_count=city_sample_data['tourist_count'],
                 tourist_growth=city_sample_data['tourist_growth'],
                 description=city_sample_data['description'])