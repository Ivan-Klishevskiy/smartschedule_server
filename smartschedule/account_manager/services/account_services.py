from ..models import UserProfile, Hobby

import geonamescache
import country_converter as coco
import re


def get_user_profile(user):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None
    

def get_all_hobby():
    try:
        hobbies = Hobby.objects.all()
        return hobbies
    except Hobby.DoesNotExist:
        return None
    
def get_list_location_by_query(query):
    gc = geonamescache.GeonamesCache()
    cities = gc.search_cities(
        query, case_sensitive=False, contains_search=True)
    
    locations = list()
    pattern = re.compile(f"^{re.escape(query)}", re.IGNORECASE | re.ASCII)
    cities = [city for city in cities if pattern.match(city['name'])]
    for city in cities[:10]:
        country_name = coco.convert(names=city['countrycode'], to='name_short')
        locations.append(f"{country_name}, {city['name']}")

    return locations