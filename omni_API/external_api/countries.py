import urllib.request, json

from app import app

from flask import g

import logging

log = logging.getLogger(__name__)

# from flask_caching import Cache  # Import Cache from flask_caching module

# cache = Cache(app) 

# from redis import Redis

# def get_redis_obj():
#     return redis.StrictRedis(host='redis', port=6379, decode_responses=True)

COUNTRIES_API_URL = app.config.get("COUNTRIES_API_URL",[])

# @cache.cached(timeout=3600, query_string=True)
def get_all_countries(refresh=False):
    try:
        countries_list = getattr(g,'_countries',None)
        if countries_list is None or refresh is True:
            url = COUNTRIES_API_URL+"all"
            response = urllib.request.urlopen(url)
            data = response.read()
            countries = json.loads(data)
            
            # redis_obj = get_redis_obj()
            # country_key = "COUNTRIES"
            countries_list={}
            for country_data in countries:
                cioc = country_data.get("cioc","")
                cca2 = country_data.get("cca2","")
                country_name = country_data.get("name",{})
                currencies = country_data.get("currencies",{})
                languages = country_data.get("languages",{})
                timezones = country_data.get("timezones",{})
                region = country_data.get("region","")
                country = {"country_official_name": country_name.get("official",""), "currencies": currencies, "languages":languages, "timezones": timezones, "region": region}
                countries_list[cioc]= country

            g._countries = countries_list
            # log.error("countries ", json.dumps(countries_list))
        
        return {"error":False, "message":"Country data fetched successfully!","countries_list":countries_list}

    except Exception as e:
        log.error(str(e))
        return {"error":True, "message":str(e),"countries_list":{}}

# @cache.cached(timeout=3600, query_string=True)
def get_single_country(user):
    try:
        cioc = user.get("country","")
        log.error("country_data cioc "+ cioc)
        if cioc:
            url = COUNTRIES_API_URL+f"alpha/{cioc.lower()}"
            log.error("country_data url "+ url)
            response = urllib.request.urlopen(url)
            data = response.read()
            country_data = json.loads(data)
            if type(country_data) == list:
                country_data = country_data[0]
            # redis_obj = get_redis_obj()
            # country_key = "COUNTRIES"
            log.error("country_data ", json.dumps(country_data))
            country_name = country_data.get("name",{})
            currencies = country_data.get("currencies",{})
            languages = country_data.get("languages",{})
            timezones = country_data.get("timezones",{})
            region = country_data.get("region","")
            country = {"country_official_name": country_name.get("official",""), "currencies": currencies, "languages":languages, "timezones": timezones, "region": region}
            # redis_key = f"{country_key}:{cioc}"
            # redis_obj.hmset(redis_key, json.dumps(country))
            # redis_obj.expire(redis_key, 3600)
            countries_list = getattr(g,'_countries',None)
            
            countries_list[cioc] = country
            g._country = countries_list
            return {"error":False, "message":"Country data fetched successfully!","country_data":country}
        else:
            return {"error":True, "message":"Country code cannot be empty.","country_data":{}}
        
    except Exception as e:
        log.error(str(e))
        return {"error":True, "message":str(e),"countries_list":{}}

