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


#auto create api_key when create user
api_key= models.signals.post_save.connect(create_api_key, sender=User)


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        #must authorization : create profile(user+ detail)
        authorization = Authorization()
        excludes = ["password"]
        allowed_methods = ["post","put"]
    
    
#create profie( = user + other information of user) 
class CreateUserResource(ModelResource):
    """
            1. register accout(User)
                exmaple:
              {
                	"user":{
                	"username":"nguyenthia2223",
                	"password":"111111aA@",
                	"first_name":"nguyen thi",
                	"last_name":"A",
                	"email":"nguyenthia@gmail.com"
                	},
                	
                	"birthday":"1994-09-01",
                	"address":"dn"
                }
               }
    """
    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)
    
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'account/create'
        allowed_methods =["post"]
        
        authorization = Authorization() 
        #return json  when create user
        always_return_data = True   
    
   
#see profile of users    
class ProfileResource(ModelResource):
    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile/see'
        allowed_methods =["get"]
        authentication = ApiKeyAuthentication()
        
    
    #return json hava address : upper ~~
    def dehydrate_address(self, bundle):
        return bundle.data['address'].upper()
    

# update profile
class UpdateProfileResource(ModelResource):
    user = tastypie.fields.ForeignKey(UserResource, 'user', full=True)
    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile/update'
        allowed_methods =["put","get"]
        excludes = ['username']
        authentication = ApiKeyAuthentication()
        authorization = Authorization()
        always_return_data = True 
        
    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(id=bundle.request.user.id).select_related()
        
    
    # def get_list(self, request, **kwargs):
    #     kwargs["pk"] = request.user.profile.pk
    #     return super(UpdateProfileResource, self).get_detail(request, **kwargs)
        



#login return data of user and api_key(use for other request after login)
class LoginResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'login'
        allowed_methods = ['get']
        excludes = [ 'password']
        authentication = BasicAuthentication()
    
    #return data of user and api_key
    def dehydrate(self, bundle):
        print(bundle.obj.api_key)
        bundle.data['key'] = bundle.obj.api_key.key
        return bundle
    
    
    ## Since there is only one user profile object, call get_detail instead
    def get_list(self, request, **kwargs):
        kwargs["pk"] = request.user.profile.pk
        return super(LoginResource, self).get_detail(request, **kwargs)
    
    #or
    # def authorized_read_list(self, object_list, bundle):
    #     return object_list.filter(id=bundle.request.user.id).select_related()
    


    

        
        
    

    
        
        