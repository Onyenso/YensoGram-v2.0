from .base import *
import django_on_heroku
from decouple import config

SECRET_KEY = config("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = ["yensogram-v2.0.herokuapp.com"]

django_on_heroku.settings(locals(), staticfiles=False)
del DATABASES["default"]["OPTIONS"]["sslnode"] # optional