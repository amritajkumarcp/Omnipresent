class Config(object):
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'database.db'
    REGIONS = ["Asia", "Europe"] # configurable that can accept more regions that needs extra country specific data
    COUNTRIES_API_URL = "https://restcountries.com/v3.1/"
    CACHE_TYPE = "SimpleCache",  # Flask-Caching related configs
    CACHE_DEFAULT_TIMEOUT = 86400

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
