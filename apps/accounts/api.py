from tastypie.resources import ModelResource
from apps.accounts.models import Profile, Friend
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, Authentication, MultiAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import tastypie
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

# import signal: once a while, user register, create api_key
from .singals import *


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        # must authorization : create profile(user+ detail)
        authorization = Authorization()
        excludes = ["password"]
        allowed_methods = ["get"]

    def dehydrate(self, bundle):
        print("A")
        print(bundle)
        bundle.data["user"] = bundle.data["username"]

        return bundle.data


class AuthenResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = "authen"

    def prepend_urls(self):
        from django.conf.urls import url
        from tastypie.utils import trailing_slash
        return [
            url(r"^(?P<resource_name>%s)/register%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('register'), name="api_register"),

            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name="api_login"),

            url(r"^(?P<resource_name>%s)/logout%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('logout'), name="api_logout"),

        ]

    def register(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        print(data)
        username = data["username"]
        password = data["password"]
        email = data["email"]
        # validation : username and pass,email: common package
        # ..
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        profile = data["profile"]
        address = profile["address"]
        birthday = profile["birthday"]
        profile = Profile(user=user, birthday=birthday, address=address)
        profile.save()
        # validation email and profile: common package
        # ..

        print(username, password, email, profile)
        return self.create_response(request, {"message": profile})

    def logout(self, request, **kwargs):
        print("bắt đầu")
        """
        A new end point to logout the user using the django login system
        """
        self.method_check(request, allowed=['get'])
        print(request.user)
        if request.user and request.user.is_authenticated():
            logout(request)
            print(request.user)

            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False,
                                                  'error_message': 'You are not authenticated, %s' % request.user.is_authenticated()})

    def login(self, request, **kwargs):
        from tastypie.http import HttpUnauthorized, HttpForbidden
        from tastypie.models import ApiKey

        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        # validation here before authenticate
        # ..

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                print(dir(user))
                return self.create_response(request, {
                    "apikey ": user.api_key.key,
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,

                })
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'disabled',
                }, HttpForbidden)
        else:
            return self.create_response(request, {
                'success': False,
                'reason': 'incorrect',
            }, HttpUnauthorized)
