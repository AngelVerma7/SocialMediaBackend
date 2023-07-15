from django.db import models
from userprofile.models import *
from feeds.models import *

class Comment(models.Model):
    commentUser=models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    commentPost=models.ForeignKey(Feed,on_delete=models.CASCADE)
    entry=models.TextField()
    date=models.DateTimeField( auto_now_add=True)
