import redis

# Default values.
FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0


def from_settings(settings):
    host = settings.get('FILTER_HOST', FILTER_HOST)
    port = settings.get('FILTER_PORT', FILTER_PORT)
    return redis.Redis(host=host, port=port)


def from_settings_filter(settings):
    host = settings.get('FILTER_HOST', FILTER_HOST)
    port = settings.get('FILTER_PORT', FILTER_PORT)
    db = settings.get('FILTER_DB', FILTER_DB)
    return redis.Redis(host=host, port=port, db=db)