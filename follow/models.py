from django.db import models
from django.contrib.auth.models import User
# from userprofile.models import *

class Follow(models.Model):
    follower=models.ForeignKey(User, on_delete=models.CASCADE,related_name="followings")
    leader=models.ForeignKey( User, on_delete=models.CASCADE,related_name="followers")
    startDate=models.DateField( auto_now_add=True)