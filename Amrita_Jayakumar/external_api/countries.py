import urllib.request, json

from app import app

from flask import g

import logging

log = logging.getLogger(__name__)

from flask_caching import Cache  # Import Cache from flask_caching module

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

COUNTRIES_API_URL = app.config.get("COUNTRIES_API_URL",[])

@cache.cached(timeout=86400, query_string=True) # caching output for 24 Hours from the first hit.
def get_all_countries(refresh=False):
    try:
        countries_list = cache.get('countries')
        if countries_list is None or refresh is True: #if not cached or deliberate refresh required, then hit the countries API
            url = COUNTRIES_API_URL+"all"
            response = urllib.request.urlopen(url)
            data = response.read()
            countries = json.loads(data)
            
            countries_list={}
            for country_data in countries:
                cioc = country_data.get("cioc","")
                cca2 = country_data.get("cca2","")
                country_name = country_data.get("name",{})
                currencies = country_data.get("currencies",{})
                languages = country_data.get("languages",{})
                timezones = country_data.get("timezones",{})
                region = country_data.get("region","")
                country = {"country_official_name": country_name.get("official",""), "currencies": currencies, "languages":languages, "timezones": timezones, "region": region, "cca2": cca2}
                countries_list[cioc]= country

            cache.set("countries",countries_list)
        
        return {"error":False, "message":"Country data fetched successfully!","countries_list":countries_list}

    except Exception as e:
        return {"error":True, "message":str(e),"countries_list":{}}

def get_single_country(user):
    try:
        cioc = user.get("country","")
        if cioc:
            url = COUNTRIES_API_URL+f"alpha/{cioc.lower()}"
            response = urllib.request.urlopen(url)
            data = response.read()
            country_data = json.loads(data)
            if type(country_data) == list:
                country_data = country_data[0]
            country_name = country_data.get("name",{})
            currencies = country_data.get("currencies",{})
            languages = country_data.get("languages",{})
            timezones = country_data.get("timezones",{})
            region = country_data.get("region","")
            country = {"country_official_name": country_name.get("official",""), "currencies": currencies, "languages":languages, "timezones": timezones, "region": region}
            countries_list = cache.get('countries')
            
            countries_list[cioc] = country
            cache.set("countries", countries_list)
            return {"error":False, "message":"Country data fetched successfully!","country_data":country}
        else:
            return {"error":True, "message":"Country code cannot be empty.","country_data":{}}
        
    except Exception as e:
        return {"error":True, "message":str(e),"countries_list":{}}

