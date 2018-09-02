from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db import models
from tastypie.models import create_api_key

# #auto create api_key when create user
api_key = models.signals.post_save.connect(create_api_key, sender=User)
