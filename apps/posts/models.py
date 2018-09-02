from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    content = models.TextField(max_length=2000)
    image = models.ImageField(upload_to='media/%Y/%m/%d/')
    author = models.ForeignKey(User)
    # count of like in this  post
    count_like = models.IntegerField(default=0)
    # count of comment in this  post
    count_comment = models.IntegerField(default=0)

    def __str__(self):
        return str(self.author)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    content = models.CharField(max_length=200)
    commenter = models.ForeignKey(User)

    def __str__(self):
        return str(self.post)


class Like(models.Model):
    post = models.ForeignKey(Post)
    liker = models.ForeignKey(User)

    def __str__(self):
        return str(self.post)
