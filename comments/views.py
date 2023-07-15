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



class CommentByIdView(APIView):
    def post(self,request):
        if "postId" not in request.data:
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)
        postId=request.data["postId"]
        comment=Comment.objects.filter(commentPost=postId)
        data=CommentSerializer(comment,many=True)
        return Response(data.data)
class AddCommentView(APIView):
    # need a edit
    authentication_classes=[JWTAuthentication,]
    def post(self,request):
        print(request.data)
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        userprofile=UserProfile.get_profile_by_user(request.user)
        

        if "commentPost" not in request.data or "entry" not in request.data:
            return Response(status=status.HTTP_302_FOUND)
        feed=Feed.objects.filter(id=request.data["commentPost"]).first()
        if not feed:
            return Response(status=status.HTTP_302_FOUND)


        obj=Comment(commentUser=userprofile,
                    commentPost=feed,
                    entry=request.data["entry"])
        obj.save()
        # obj=CreateCommentSerializer(data=request.data)
        # print("hiii")
        # if obj.is_valid():
        #     print("hiii")
        #     comment=obj.save()
        #     obj=Comment(comment,user)
        #     obj.save()

        comment=CommentSerializer(obj)
        return Response(data=comment.data)
        
         