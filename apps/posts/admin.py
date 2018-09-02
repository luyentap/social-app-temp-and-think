from django.contrib import admin
from apps.posts.models import Post, Like, Comment

# Register your models here.


admin.register(Post)(admin.ModelAdmin)
admin.register(Like)(admin.ModelAdmin)
admin.register(Comment)(admin.ModelAdmin)
