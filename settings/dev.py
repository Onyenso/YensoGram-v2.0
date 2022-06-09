from distutils.debug import DEBUG
from .base import *

SECRET_KEY = "abc" # dosen't really matter in development
DEBUG = True
ALLOWED_HOSTS = ["*"] # all urls allowed

