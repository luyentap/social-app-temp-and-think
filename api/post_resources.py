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

#get all post of user: get,update,delete,create
class PostByUserResource(ModelResource):
    author = tastypie.fields.ForeignKey(UserResource, 'author')
    class Meta:
        resource_name = 'my_post'
        queryset = Post.objects.all()
        method_allow =["get","put","delete","post"]
        authentication = ApiKeyAuthentication()
        authorization = PostObjectsOnlyAuthorization()
        always_return_data = True
        
    # def authorized_read_list(self, object_list, bundle):
    #     # print(dir(bundle.request.user))
    #     # print(bundle.request.user.id)
    #     # profile = Profile.objects.filter(user=bundle.request.user.id)
    #     return object_list.filter(author=bundle.request.user.id).select_related()
        
        
#get all post by friend?? hide in wall (hien thi tren tuong)
class PostsResource(ModelResource):
    author = tastypie.fields.ForeignKey(UserResource, 'author')
    class Meta:
        resource_name = 'posts'
        queryset = Post.objects.all()
        method_allow =["get"]
        authentication = ApiKeyAuthentication()

#get all comment của chinh nguoi do(myactivity)

#get all comment : can su dung cho resources khac(CommentInPostResource) hay ko
class CommentsResource(ModelResource):
    post = tastypie.fields.ForeignKey(PostsResource, 'post')
    commenter = tastypie.fields.ForeignKey(UserResource, 'commenter')
    class Meta:
        resource_name = 'all_comments'
        queryset = Comment.objects.all()
        method_allow =["get"]
        authentication = ApiKeyAuthentication()

#In a post:
# see all comment:
#create comment: post/comment/?
#update:         
#delete comment: post/comment
class CommentInPostResource(ModelResource):
    post = tastypie.fields.ForeignKey(PostsResource, 'post')
    commenter = tastypie.fields.ForeignKey(UserResource, 'commenter')
    class Meta:
        resource_name = "comments"
        queryset = Comment.objects.all()
        
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True
        # detail_uri_name = 'id'

    def prepend_urls(self):
        from django.conf.urls import url
        return [
            
            url(r"^post/(?P<post_id>[\w\d_.-]+)/(?P<resource_name>%s)/(?P<id_comment>[\w\d_.-]+)" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^post/(?P<post_id>[\w\d_.-]+)/(?P<resource_name>%s)" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            
        ]
        
    def dispatch_list(self, request, **kwargs):
        # bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
        # obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        child_resource = CommentInPostResource()
        # print(dir(kwargs.items))
        # kwargs["post_id"] = 1
        post_id = kwargs.pop('post_id')
        print(post_id)
        # print(dir(child_resource.get_list(request, post_id=post_id)))
        print(child_resource.get_list(request, post_id=post_id).content)
        return child_resource.get_list(request, post_id =post_id)
    
    def dispatch_detail(self, request, **kwargs):
        # bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
        # obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        child_resource = CommentInPostResource()    
        post_id = kwargs.pop('post_id')
        print(post_id)
        id = kwargs.pop('id_comment')
        print("id"+id)
        print(self.get_object_list(request).filter(post_id=post_id))
        return self.get_object_list(request).filter(post_id=post_id)
    
    
    
    # def obj_create(self, bundle, request=None, **kwargs):
    #     #incretate number comment in post
        
    #     return super(CommentInPostResource, self).obj_create(bundle, request, user=request.user)
    
    # def get_list(self, request, **kwargs):
    #     kwargs["pk"] = request.GET["id_post"]
    #     return super(CommentInPostResource, self).get_detail(request, **kwargs)
        
    # def authorized_read_list(self,object_list, bundle):
    #     # print(dir(bundle.request))
    #     id_post = bundle.request.GET["id_post"]
        
    #     return super(CommentInPostResource,self).authorized_read_list(object_list, bundle)
      
        

        