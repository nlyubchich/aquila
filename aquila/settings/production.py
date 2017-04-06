from .development import *
import dj_database_url

SECRET_KEY = os.environ['APP_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = [os.environ['APP_ALLOWED_HOST']]

DATABASES = {
    'default': dj_database_url.config(conn_max_age=500)
}
GOOGLE_MAPS_API_KEY = os.environ['APP_GOOGLE_MAPS_API_KEY']
