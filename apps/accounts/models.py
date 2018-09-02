from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User)

    birthday = models.DateField()
    address = models.CharField(max_length=100)

    def __str__(self):
        return str(self.user.get_full_name())


class Friend(models.Model):
    """
    status of friends
        0: reset status
        1: is a request friend
        2: accept  friend
    """
    STATUS_FRIEND = (
        ('0', 'reset_request'),
        ('1', 'is_request'),
        ('2', 'accept_friend'),
    )

    user = models.ForeignKey(User, related_name="user")
    friend = models.ForeignKey(User, related_name="friend")
    status = models.CharField(max_length=1, choices=STATUS_FRIEND)
    """
    is a friend: check 
        0:not a friend
        1: a friend
    """
    is_friend = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)
