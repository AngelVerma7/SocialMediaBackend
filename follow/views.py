from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from .models import *
# from .serializers import *


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from userLogin.serializers import *

class StartFollowingView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        user=request.user
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "username" not in request.data:
            return Response({"message":"username should be present in the request."},status=status.HTTP_400_BAD_REQUEST)
        userId=request.data["username"]
        leader=User.objects.filter(username=userId).first()
        if not leader:
            return Response({"message":"There is no user with this username"},status=status.HTTP_400_BAD_REQUEST)
        obj=Follow.objects.filter(leader=leader,follower=user).first()
        if obj:
            print("already following")
            return Response({"message":"User currently follow this user"},status=status.HTTP_200_OK)   
        obj=Follow(leader=leader,follower=user)
        obj.save()
        return Response({"message":"User started following this user"},status=status.HTTP_200_OK)   
        

        

