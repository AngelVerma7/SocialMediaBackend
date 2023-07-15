from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class UserProfileSerializer(serializers.ModelSerializer):
    username= serializers.CharField(read_only=True, source="profileuser.username")
    first_name= serializers.CharField(read_only=True, source="profileuser.first_name")
    last_name= serializers.CharField(read_only=True, source="profileuser.last_name")

    class Meta:
        model=UserProfile
        fields="__all__"
        extra_fields = ['username','first_name','last_name']
class ProfileUpdateSerializer(serializers.ModelSerializer):
    # username= serializers.CharField(read_only=True, source="profileuser.username")
    first_name= serializers.CharField(read_only=True, source="profileuser.first_name")
    last_name= serializers.CharField(read_only=True, source="profileuser.last_name")

    class Meta:
        model=UserProfile
        fields=("desc","first_name","last_name")
        extra_fields = ['first_name','last_name']
        depth=1


