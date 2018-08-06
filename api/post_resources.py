from tastypie.resources import ModelResource
from app.models import Profile,Post
from django.contrib.auth.models import User
from django.db import models
from tastypie.models import create_api_key
from tastypie.authentication import ApiKeyAuthentication,BasicAuthentication,Authentication,MultiAuthentication
from tastypie.authorization import Authorization,DjangoAuthorization
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized
import tastypie
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from account_resources import ProfileResource


class PostResource(ModelResource):
    author = tastypie.fields.ForeignKey(ProfileResource, 'author', full=True)
    class Meta:
        resource_name = 'post'
        queryset = Post.objects.all()
        authentication = ApiKeyAuthentication()
        
        
    def authorized_read_list(self, object_list, bundle):
        # print(dir(bundle.request.user))
        # print(bundle.request.user.id)
        profile = Profile.objects.filter(user=bundle.request.user.id)
        return object_list.filter(author=profile).select_related()
        