from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    profileuser=models.ForeignKey(User,  on_delete=models.CASCADE)
    desc=models.TextField()
    avatar=models.ImageField( upload_to='media/profile', height_field=None, width_field=None, max_length=None)
    link=models.TextField()
    def get_profile_by_user(user):
        obj=UserProfile.objects.filter(profileuser=user)
        if(len(obj)):
            return obj[0]
        return None
    def __str__(self):
        return self.profileuser.username


