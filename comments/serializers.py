from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from comments.models import *


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="commentUser.profileuser.username")
    avatar = serializers.CharField(read_only=True, source="commentUser.avatar")
    class Meta:
        model=Comment
        fields="__all__"
        extra_fields=["username","useravatar"]

class CreateCommentSerializer(serializers.ModelSerializer):
    
     class Meta:
          model=Feed
          fields="__all__"
