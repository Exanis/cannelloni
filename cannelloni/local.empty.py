# -*- coding: utf8 -*-

"Local settings for cannelloni"

from .settings import *

SECRET_KEY = ''
DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}