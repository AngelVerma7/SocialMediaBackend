from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from comments.models import *


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="commentUser.profileuser.username")
    avatar = serializers.CharField(read_only=True, source="commentUser.avatar")
    def to_representation(self, instance):
            representation = super().to_representation(instance)
            # feeduser=representation['feeduser']
            # feedpost=representation['id']
            # print(feeduser)
            # likes=Like.objects.filter(likedpost=feedpost).count()
            # representation["likes"]=likes


            # comments=Comment.objects.filter(commentPost=feedpost).count()
            likes=CommentLike.objects.filter(likeOn=representation["id"]).count()
            replies=CommentReply.objects.filter(commentOn=representation["id"]).count()
            representation["likes"]=likes
            representation["replies"]=replies
            return  representation
    class Meta:
        model=Comment
        fields="__all__"
        extra_fields=["username","useravatar"]

class CreateCommentSerializer(serializers.ModelSerializer):
     class Meta:
          model=Feed
          fields="__all__"

class CommentReplySerializer(serializers.ModelSerializer):
 
    def to_internal_value(self, data):
        user = self.context['request'].user
        userProfile=UserProfile.objects.filter(profileuser=user).first()
        if not userProfile:
              return super().to_internal_value(data)
             
        if "entry" not in data or "commentOn" not in data:
             return super().to_internal_value(data)
        commentOn=data["commentOn"]
        commentOn=Comment.objects.filter(id=commentOn).first()
        print(commentOn)
        print(userProfile)
        print(data["entry"])
        if not commentOn:
            return super().to_internal_value(data)
        print("ye step bhi ho gya")
     #    instance=CommentReply.objects.get_or_create(
     #         commentUser=userProfile,
     #         entry=data["entry"],
     #         commentOn=commentOn
     #    )
        data["commentOn"]=commentOn.id
        data["commentUser"]=userProfile.id
        print(data)
        return super().to_internal_value(data)

    class Meta:
        model=CommentReply
        fields=("entry","commentOn","commentUser")
        
        
class CommentReplyViewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True, source="commentUser.profileuser.username")
    avatar = serializers.CharField(read_only=True, source="commentUser.avatar")
    class Meta:
        model=CommentReply
        fields="__all__"
        extra_fields=["username","useravatar"]