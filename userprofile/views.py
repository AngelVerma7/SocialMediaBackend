from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.parsers import MultiPartParser

from .models import *
from .serializers import *


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.tokens import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from userLogin.serializers import *
from feeds.models import * 
from feeds.serializers import * 


class ProfileView(APIView):
    serializer_class=UserProfileSerializer
    def get(self,request,username):
        userobj=User.objects.filter(username=username).first()
        if not userobj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userobj=UserProfile.get_profile_by_user(userobj)
        if userobj:
            userData=UserProfileSerializer(userobj) 
            return Response(userData.data)
        return Response(status=status.HTTP_403_FORBIDDEN)
    


    def post(self,request):
        if "username" not in request.data: 
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)
        username=request.data["username"]
        userobj=User.objects.filter(username=username).first()
        if not userobj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userobj=UserProfile.get_profile_by_user(userobj)
        if userobj:
            userData=UserProfileSerializer(userobj) 
            return Response(userData.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

class UpdateProfile(APIView):
    parser_classes=[MultiPartParser]
    authentication_classes=[JWTAuthentication]
    serializer_class=ProfileUpdateSerializer
    def post(self,request):
        userprofile=UserProfile.get_profile_by_user(request.user)
        if not userprofile:
            return Response(status=status.HTTP_403_FORBIDDEN)
        user=UserNameSerializer(request.user,data=request.data)
        obj=ProfileUpdateSerializer(userprofile,data=request.data)
        if obj.is_valid() and user.is_valid():
            obj.save()
            user.save()

            return Response()
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UserFeeds(APIView):
    def get(self,request):
        Response(status=status.HTTP_300_MULTIPLE_CHOICES)
    def post(self,request):
        if "username" not in request.data: 
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        user=User.objects.filter(username=request.data["username"]).first()
        
        if not user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        profile=UserProfile.objects.filter(profileuser=user).first()
        if not profile:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        feeds=Feed.objects.filter(feeduser=profile)
            

        # feeds=Feed.objects.filter(feeduser=request.data["username"])
        data=FeedSerializer(feeds,many=True)

        return Response(data.data)  

