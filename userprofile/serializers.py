from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from feeds.models import *
from follow.models import *
from follow.views import *

class UserProfileSerializer(serializers.ModelSerializer):
    username= serializers.CharField(read_only=True, source="profileuser.username")
    first_name= serializers.CharField(read_only=True, source="profileuser.first_name")
    last_name= serializers.CharField(read_only=True, source="profileuser.last_name")
    userId=serializers.CharField(read_only=True, source="profileuser.id")
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        follower=Follow.objects.filter(follower=representation['userId']).count()
        representation["follower"]=follower
        leader=Follow.objects.filter(leader=representation['userId'])
        representation["leader"]=len(leader)
        feeds=Feed.objects.filter(feeduser=representation['id']).count()
        print(feeds)
        representation["feeds"]=feeds
        # user = self.context['request'].user
        # isFollowing=Follow.objects.filter(follower=representation['userId'],leader=user).count()
        # representation["isFollowing"]=isFollowing
        # isMe=0
        # if str(user.id)==str(representation["userId"]):
            # isMe=1
        # representation["isMe"]=isMe

        

        return representation
        
    class Meta:
        model=UserProfile
        fields="__all__"
        extra_fields = ['username','first_name','last_name',"userId"]

class UserProfileDetailSerializer(serializers.ModelSerializer):
    username= serializers.CharField(read_only=True, source="profileuser.username")
    first_name= serializers.CharField(read_only=True, source="profileuser.first_name")
    last_name= serializers.CharField(read_only=True, source="profileuser.last_name")
    userId=serializers.CharField(read_only=True, source="profileuser.id")
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        follower=Follow.objects.filter(follower=representation['userId']).count()
        representation["follower"]=follower
        leader=Follow.objects.filter(leader=representation['userId'])
        representation["leader"]=len(leader)
        feeds=Feed.objects.filter(feeduser=representation['id']).count()
        print(feeds)
        representation["feeds"]=feeds
        user = self.context['request'].user
        isFollowing=Follow.objects.filter(follower=user,leader=representation['userId']).count()
        representation["isFollowing"]=isFollowing
        isMe=0
        if str(user.id)==str(representation["userId"]):
            isMe=1
        representation["isMe"]=isMe
        degree=followDegreeFun( self.context['request'],target=representation["userId"])
        representation["degree"]=degree

        

        return representation
        
    class Meta:
        model=UserProfile
        fields="__all__"
        extra_fields = ['username','first_name','last_name',"userId"]

class ProfileUpdateSerializer(serializers.ModelSerializer):
    # username= serializers.CharField(read_only=True, source="profileuser.username")
    first_name= serializers.CharField(read_only=True, source="profileuser.first_name")
    last_name= serializers.CharField(read_only=True, source="profileuser.last_name")

    class Meta:
        model=UserProfile
        fields=("desc","first_name","last_name","avatar")
        extra_fields = ['first_name','last_name']
        depth=1


