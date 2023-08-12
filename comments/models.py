from django.db import models
from userprofile.models import *
from feeds.models import *

class Comment(models.Model):
    commentUser=models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    commentPost=models.ForeignKey(Feed,on_delete=models.CASCADE)
    entry=models.TextField()
    date=models.DateTimeField( auto_now_add=True)
class CommentReply(models.Model):
    commentUser=models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    commentOn=models.ForeignKey(Comment,on_delete=models.CASCADE)
    entry=models.TextField()
    date=models.DateTimeField( auto_now_add=True)

# class CommentLike(models.Model):
#     commentUser=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
#     likeOn=models.ForeignKey(Comment,on_delete=models.CASCADE)
#     class Meta:
#         unique_together=('commentUser','likeOn')
