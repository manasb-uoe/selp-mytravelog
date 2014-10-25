from bs4 import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import urllib
import re
import pickle
import os


class City(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# fetches city stats from Euromonitor ranking table
def get_city_stats():
    link = "http://blog.euromonitor.com/2014/01/euromonitor-internationals-top-city-destinations-ranking.html"
    cities = []
    f = None
    try:
        f = urllib.urlopen(link)
        html = f.read()
        soup = BeautifulSoup(html)
        all_rows = soup.find_all('tr')
        required_rows = all_rows[2:len(all_rows)-9]
        for row in required_rows:
            columns = row.find_all('p')
            name = smart_str(columns[0].text)
            # East Province does not exist on wikipedia/wikitravel    
            if name == "East Province":
                name = "Eastern Province"
                url_name = "Eastern_Province,_Saudi_Arabia"
            else:
                url_name = re.sub(r'\s', '_', name)
            country_name = smart_str(columns[1].text)
            tourist_count = int(float(re.sub(r"[^a-zA-Z0-9\.]", '', smart_str(columns[3].text))) * 1000)
            growth = float(re.sub(r"[^a-zA-Z0-9\.-]", '', smart_str(columns[4].text)))
            cities.append(City(name=name, url_name=url_name, country_name=country_name, tourist_count=tourist_count, tourist_growth=growth))
        return cities
    except Exception as e:
        print repr(e)
    finally:
        if f is not None:
            f.close()


# fetches first few paragraph (while total words < 200) from wikitravel/wikipedia (depends on the base_link provided)
def get_city_info(cities, base_link):
    f = None
    try:
        for city in cities:
            link = base_link + city.url_name
            f = urllib.urlopen(link)
            html = f.read()
            soup = BeautifulSoup(html)
            all_p = soup.find_all('p')
            info = ""
            p_count = len(all_p)
            for index, value in enumerate(all_p):
                if len(info.split(' ')) < 200 and index < p_count-1:
                    p_text = smart_str(value.text) 
                    if len(p_text.split(" ")) > 15:  # only consider paragraphs with more than 15 words
                        info += p_text
            city.info = info
            print city.name
        return cities
    except Exception as e:
        print repr(e)
    finally:
        f.close()


# serializes the provided list of cities in a file named filename, within the same directory
def serialize(cities, fileName):
    outfile = None
    try:
        info_path = os.path.join(os.path.dirname(__file__), fileName)
        outfile = open(info_path, 'wb')
        pickle.dump(cities, outfile)
    except Exception as e:
        print repr(e)
    finally:
        outfile.close()


# deserializes the list of cities from a file named filename, within the same directory
def deserialize(fileName):
    infile = None
    try:
        info_path = os.path.join(os.path.dirname(__file__), fileName)
        infile = open(info_path, 'rb')
        cities = pickle.load(infile)
        return cities
    except Exception as e:
        print repr(e)
    finally:
        infile.close()


# (only used for testing)
# write city name, url_name and info in a readable form, to a file named filename, within the same directory
def write_to_file_readable(cities, file_name):
    outfile = None
    try:
        info_path_readable = os.path.join(os.path.dirname(__file__), file_name)
        outfile = open(info_path_readable, 'wb')
        for city in cities:
            outfile.write(city.name + "\n")
            outfile.write(city.url_name + "\n")
            outfile.write(city.info + "\n\n")
    except Exception as e:
        print repr(e)
    finally:
        outfile.close()


# urls and file names
wikipedia = "info_dump_wikipedia.txt"
wikipedia_readable = "info_dump_wikipedia_readable.txt"
wikitravel = "info_dump_wikitravel.txt"
wikitravel_readable = "info_dump_wikitravel_readable.txt"
base_link_wikipedia = "http://en.wikipedia.org/wiki/"
base_link_wikitravel = "http://wikitravel.org/en/"


# starting point
if __name__ == "__main__":
    cities = get_city_stats()
    final_cities = get_city_info(cities, base_link_wikipedia)
    serialize(final_cities, wikipedia)
    final_cities = deserialize(wikipedia)
    write_to_file_readable(final_cities, wikipedia_readable)
