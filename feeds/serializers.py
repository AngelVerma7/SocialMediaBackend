from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from comments.models import * 

class FeedSerializer(serializers.ModelSerializer):
     userdesc= serializers.CharField(read_only=True, source="feeduser.desc")
     username= serializers.CharField(read_only=True, source="feeduser.profileuser.username")
     firstname= serializers.CharField(read_only=True, source="feeduser.profileuser.first_name")
     lastname= serializers.CharField(read_only=True, source="feeduser.profileuser.last_name")
     # desc= serializers.CharField(read_only=True, source="feeduser.desc")
     useravatar= serializers.CharField(read_only=True, source="feeduser.avatar")
 
     def to_representation(self, instance):
            representation = super().to_representation(instance)
            feeduser=representation['feeduser']
            feedpost=representation['id']
            print(feeduser)
            is_liked=-1
            representation["is_liked"]=-1
            representation["isLiked"]=0
            if self.context and not self.context["request"].user.is_anonymous:
                  is_liked=Like.objects.filter(likedby=self.context['request'].user,likedpost=feedpost).first()
                  representation["isLiked"]=1 if is_liked else 0
            likes=Like.objects.filter(likedpost=feedpost).count()
            representation["likes"]=likes

           
            comments=Comment.objects.filter(commentPost=feedpost).count()       
            representation["comments"]=comments
            return  representation
     class Meta:
        model=Feed
        fields="__all__"
        extra_fields = ["username",
                        'first_name','last_name'
                        'useravatar','userdesc',
                        ]
class LikeFeedSerializer(serializers.ModelSerializer):
     def to_internal_value(self, data):
        if "postid" not in data:
             return super().to_internal_value(data)
        post=Feed.objects.filter(id=data["postid"]).first()
        if not post:
             return super().to_internal_value(data)
        user = self.context['request'].user
        instance = Like.objects.get_or_create(
            likedby=user,
            likedpost=post
        )
        return super().to_internal_value(instance)
     class Meta:
          model=Like
          fields="__all__"
class CreateFeedSerializer(serializers.ModelSerializer):
     # avatar = serializers.ImageField(required=True)
     # feeduser= serializers.ReadOnlyField(source='creator.id')
     def to_internal_value(self, data):
        user = self.context['request'].user
        userProfile=UserProfile.objects.filter(profileuser=user).first()
        if not userProfile:
              return super().to_internal_value(data)
        
        if "avatar" not in data:
             return super().to_internal_value(data)
        data["feeduser"]=userProfile.id
        print(data)
     #    if "desc" in self.request.data:
             
             
     #    instance=Feed.objects.get_or_create(
     #         feeduser=userProfile,
     #         avatar=data["avatar"] if "avatar" in data else None,
     #         desc=data["desc"] if "desc" in data else "",
     #         link=data["link"] if "link" in data else "",
             
     #            )
        return super().to_internal_value(data)
     class Meta:
          model=Feed
          fields=("avatar","feeduser","desc")

