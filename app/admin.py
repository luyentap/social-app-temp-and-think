from django.contrib import admin
from app.models import Profile, Friend, Post, Comment, Like

# Register your models here.
admin.site.register(Profile)
admin.site.register(Friend)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
