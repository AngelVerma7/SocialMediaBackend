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
        page=0
        if "page" in request.data:
            page=request.data["page"]
        pagesize=10
        postId=request.data["postId"]
        comment=Comment.objects.filter(commentPost=postId).order_by("-date")
        maxpage = int((len(comment) / pagesize )+ (1 if len(comment) % pagesize else 0))
        data=CommentSerializer(comment,many=True)


        if(page >=maxpage):
            return Response({"remaining comments are":0,"comments":[]})
        page = int(page % maxpage)
        objs = comment[(page) * pagesize : min(len(comment), (page + 1) *    pagesize)]
        serializer = CommentSerializer(objs, many=True)
        res=dict()
        if page==maxpage-1:
            res["remaining"]=0
        else:
            res["remaining"]=1
        res["comments"]=serializer.data    
        return Response(res)

        # return Response(data.data)
class AddCommentView(APIView):
    # need a edit
    authentication_classes=[JWTAuthentication,]
    def post(self,request):
        print(request.data)
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        userprofile=UserProfile.get_profile_by_user(request.user)
        if not userprofile:
            return Response({"message":"Not the app"})

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
    




class CommentReplyView(APIView):
     def post(self,request):
        if "commentId" not in request.data:
            return Response({"message":"please include commentId"})
        page=0
        if "page" in request.data:
            page=request.data["page"]
        pagesize=4
        commentId=request.data["commentId"]
        comment=CommentReply.objects.filter(commentOn=commentId)
        maxpage = int((len(comment) / pagesize )+ (1 if len(comment) % pagesize else 0))
        # data=CommentSerializer(comment,many=True)


        if(page >=maxpage):
            return Response({"remaining comments are":0,"comments":[]})
        page = int(page % maxpage)
        objs = comment[(page) * pagesize : min(len(comment), (page + 1) *    pagesize)]
        serializer = CommentReplyViewSerializer(objs, many=True)
        res=dict()
        if page==maxpage-1:
            res["remaining"]=0
        else:
            res["remaining"]=1
        res["commentsReply"]=serializer.data    
        print(serializer)
        return Response(res)


class AddCommentReplyView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        userprofile=UserProfile.objects.filter(profileuser=request.user).first()
        if not userprofile:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "commentOn" not in request.data or "entry" not in request.data:
            return Response(status=status.HTTP_302_FOUND)
        commentOn=Comment.objects.filter(id=request.data["commentOn"]).first()
        if not commentOn:
            return Response({"message":"There is no comment like that"})
        obj=CommentReplySerializer(context={"request": request},data=request.data)
        print(type(request.data))
        print(obj)
        if obj.is_valid():
            print("why not")
            obj.save()
            return Response({"message":"comment added successfully"})
        return Response({"message":"not a valid serializer"})
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class DeleteCommentReplyView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        userprofile=UserProfile.objects.filter(profileuser=request.user).first()
        if not userprofile:
            return Response({"message":"no such user exist"})
        if "replyId" not in request.data:
            return Response({"message":"please include replyId"})
        replyId=request.data["replyId"]
        obj=CommentReply.objects.filter(id=replyId,commentUser=userprofile).first()
        if obj:
            obj.delete()
            return Response({"message":"comment reply deleted successfully"})
        
        return Response({"message":"no such comment exist"})
    
class LikeCommentView(APIView):
       authentication_classes=[JWTAuthentication]
       def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        userprofile=UserProfile.objects.filter(profileuser=user).first()
        if not userprofile:
            return Response({"message":"no such user exist"})
        if "commentId" not in request.data:
            return Response({"message":"please include commentId"})
        comment=Comment.objects.filter(id=request.data["commentId"]).first()
        if not comment:
            return Response({"message":"no such comment exist"})
        obj=CommentLike.objects.filter(commentUser=userprofile,likeOn=comment).first()
        if obj:
            return Response({"message":"you already liked this comment"})
        obj=CommentLike(commentUser=userprofile,likeOn=comment)
        obj.save()
        return Response({"message":"comment liked succussfully"})
    
class UnlikeCommentView(APIView):
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user=request.user
        userprofile=UserProfile.objects.filter(profileuser=user).first()
        if not userprofile:
            return Response({"message":"no such user exist"})
        if "commentId" not in request.data:
            return Response({"message":"please include commentId"})
        commentReply=CommentLike.objects.filter(commentUser=userprofile,likeOn=request.data["commentId"]).first()
        if not commentReply:
            return Response({"message":"you haven't liked this comment"})
        commentReply.delete()
        return Response({"messag":"successfully unlike the comment"})

    
    

    

      

          






        
        
         