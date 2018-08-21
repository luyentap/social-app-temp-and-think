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

# class CustomPassWordAuthorization(Authorization):

#auto create api_key when create user or login,..
api_key= models.signals.post_save.connect(create_api_key, sender=User)

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        #must authorization : create profile(user+ detail)
        authorization = Authorization()
        excludes = ["password"]
        allowed_methods = ["get","post","put"]
        authentication = Authentication()
    
    
#create profie( = user + other information of user) 
class CreateUserResource(ModelResource):
    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)
    
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'account'
        allowed_methods =["post"]
        authorization = Authorization() 
        #return json  when create user
        always_return_data = True   
    
   
#see profile of users  and update profile
class ProfileResource(ModelResource):
    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        allowed_methods =["get","put"]
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True 
    
    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()
    
    #     kwargs["pk"] = request.user.profile.pk
    #     return super(UpdateProfileResource, self).get_detail(request, **kwargs)


#login return data of user and api_key(use for other request after login)
class LoginResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'login'
        allowed_methods = ['get',"delete","post"]
        excludes = [ 'password']
        authentication = BasicAuthentication()
        
    
    #return data of user and api_key
    def dehydrate(self, bundle):
        print(bundle.obj.api_key)
        bundle.data['key'] = bundle.obj.api_key.key
        return bundle
    
    
    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        print(request.user.profile)
        kwargs["pk"] = request.user.id
        return super(LoginResource, self).get_detail(request, **kwargs)
    
   
    
    def logout(self, request, **kwargs):
        """
        A new end point to logout the user using the django login system
        """
        self.method_check(request, allowed=['delete'])
        if request.user and request.user.is_authenticated():
            super(LoginResource,self).logout(request)



