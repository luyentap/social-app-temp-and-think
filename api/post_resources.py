from tastypie.resources import ModelResource
from app.models import Profile,Post,Comment
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
#fix import with python3
from api.account_resources import *
from api.autho_custom import PostObjectsOnlyAuthorization

# get all post of user: get,update,delete,create
class PostByUserResource(ModelResource):
    author = tastypie.fields.ForeignKey(UserResource, 'author')
    class Meta:
        resource_name = 'my_post'
        queryset = Post.objects.all()
        method_allow =["get","put","delete","post"]
        authentication = ApiKeyAuthentication()
        authorization = PostObjectsOnlyAuthorization()
        always_return_data = True

        
#get all post (show in wall)
class AllPostsResource(ModelResource):
    author = tastypie.fields.ForeignKey(UserResource, 'author',full=True)
    class Meta:
        resource_name = 'all_post'
        queryset = Post.objects.all()
        method_allow =["get"]
        authentication = ApiKeyAuthentication()
        
        
#Get to list post by other user
class ListPostByUserResource(ModelResource):
    author = tastypie.fields.ForeignKey(UserResource, 'author')
    class Meta:
        resource_name = 'list_post'
        queryset = Post.objects.all()
        method_allow =["get"]
        authentication = ApiKeyAuthentication()
    
    def prepend_urls(self):
        from django.conf.urls import url
        return [
            
            url(r"^(?P<resource_name>%s)/user/(?P<id_user>[\w\d_.-]+)" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            
        ]
    
    def dispatch_list(self, request, **kwargs):
        return self.get_list(request, **kwargs)
     

    def authorized_read_list(self, object_list, bundle):
        # print(bundle.request.path)
        id_user = bundle.request.resolver_match.kwargs["id_user"]
        return object_list.filter(author=id_user).select_related()
    
    def get_list(self, request, **kwargs):
        return super(ListPostByUserResource, self).get_list(request, **kwargs)
