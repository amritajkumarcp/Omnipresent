import os
class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'database.db'
    REGIONS = ["Asia", "Europe"]
    COUNTRIES_API_URL = "https://restcountries.com/v3.1/"
    CACHE_TYPE="redis"
    CACHE_REDIS_HOST="redis"
    CACHE_REDIS_PORT="6379"
    CACHE_REDIS_DB="0"
    CACHE_REDIS_URL="redis://redis:6379/0"
    CACHE_DEFAULT_TIMEOUT="500"

class ProductionConfig(Config):
    DEBUG = False
    # CACHE_TYPE = os.environ['CACHE_TYPE']
    # CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    # CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    # CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    # CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    # CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
