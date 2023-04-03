"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# New Imports

from importlib.util import find_spec
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
#from api import router

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

application = get_wsgi_application()

app = FastAPI()
app.mount("/admin", WSGIMiddleware(application))
app.mount("/static",
    StaticFiles(
         directory=os.path.normpath(
              os.path.join(find_spec("django.contrib.admin").origin, "..", "static")
         )
   ),
   name="static",
)
