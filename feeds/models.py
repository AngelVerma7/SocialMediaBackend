from django.db import models
from django.contrib.auth.models import User
from userprofile.models import *
class Feed(models.Model):
    feeduser=models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    desc=models.TextField(null=True)
    
    avatar=models.ImageField( upload_to='media/avatar', height_field=None, width_field=None, max_length=None,null=False)

    # avatar=models.userImageField( upload_to='avatar/', height_field=None, width_field=None, max_length=None)
    datecreated=models.DateTimeField( auto_now_add=True)
    edited=models.DateTimeField(auto_now=True)
    link=models.TextField(null=True)
    # def get_profile_by_user(user):
    #     obj=UserProfile.objects.filter(profileuser=user)
    #     if(len(obj)):
    #         return obj[0]
    #     return None


class Like(models.Model):
    likedby=models.ForeignKey("auth.User",  on_delete=models.CASCADE)
    likedpost=models.ForeignKey(Feed,  on_delete=models.CASCADE)
    class Meta:
        unique_together=('likedby','likedpost')
