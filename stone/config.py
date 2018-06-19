REDIS_URL = "redis://redis:6379/0"
DEBUG = True
TESTING = False

JOBS = [
    {
        'id': 'actoken_refresh',
        'func': 'actoken:refresh',
        'args': None,
        'trigger': 'interval',
        'seconds': 7000
    }
]

