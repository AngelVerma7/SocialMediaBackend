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
class UnfollowView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        if "leader" not in request.data:
            return Response({"message":"need leader for unfollow"},status=status.HTTP_400_BAD_REQUEST)
        obj=User.objects.filter(username=request.data["leader"]).first()
        if not obj:
            return Response({"message":"the leader doesn't exist"},status=status.HTTP_400_BAD_REQUEST)
        leader=obj.id
        
        obj=Follow.objects.filter(follower=user.id,leader=leader).first()
        if obj:
            print("successfully deleted")
            obj.delete()
            print("ho gya delete")
            return Response()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowDegreeView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        if "target" not in request.data:
            return Response({"message":"can not return degree without 'degree' "})
        target=User.objects.filter(username=request.data["target"]).first()
        if not target:
            return Response({"message":"This targeted user doesn't exist"})
        follow={user.id}
        
        target=target.id
        for i in range(3):
            following=Follow.objects.filter(follower__in=follow)
            for item in following:
                follow.add(item.leader.id)
            if target in follow:
                return Response({"degree":i+1})
        return Response({"degree":4})
        
def followDegreeFun(request,target:int):
    user=request.user
    # target=User.objects.filter(username=target).first()
    # if not target:
        # return 4
    follow={user.id}        
    # target=id
    target=int(target)
    for i in range(3):
        following=Follow.objects.filter(follower__in=follow)
        for item in following:
            follow.add(item.leader.id)
        if target in follow:
            return i+1
    return 4









        
    
        

