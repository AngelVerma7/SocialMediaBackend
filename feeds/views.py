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



class FeedView(APIView):
    def get(self, request, postid):
        obj = Feed.objects.filter(id=postid).first()
        if not obj:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer = FeedSerializer(obj)

        return Response(serializer.data)


class MyFeedView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        obj = Feed.objects.filter(feeduser=user)
        print(obj)
        serializer = FeedSerializer(obj, many=True)
        return Response(serializer.data)


class LikeFeedView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)        
        serializer = LikeFeedSerializer(context={"request": request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)


class UnlikeFeedView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        if "postid" in request.data:
            obj = Like.objects.filter(
                likedby=user, likedpost=request.data["postid"]
            ).first()
            if obj:
                obj.delete()
            return Response()
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class DeleteFeedView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "postid" in request.data:
            obj = Feed.objects.filter(
                id=request.data["postid"], feeduser=request.user
            ).first()
            if obj:
                obj.delete()
                return Response()
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class FeedPagesView(APIView):
    def get(self, request):
        print(request.GET)
        pagesize = 5
        page = 0
        if "page" in request.GET:
            page = int(request.GET["page"])
        feeds = Feed.objects.all()
        maxpage = int(len(feeds) / pagesize + (1 if len(feeds) % pagesize else 0))
        page = int(page % maxpage)
        objs = feeds[(page) * pagesize : min(len(feeds), (page + 1) * pagesize)]
        serializer = FeedSerializer(objs, many=True)
        return Response(serializer.data)
    def post(self, request):
        # print(request.GET)
        pagesize = 5
        page = 0
        if "page" in request.data:
            page = int(request.data["page"])
        print("the page is",page)
        feeds = Feed.objects.all().order_by("-datecreated")
        maxpage = int(len(feeds) / pagesize + (1 if len(feeds) % pagesize else 0))
        page = int(page % maxpage)
        objs = feeds[(page) * pagesize : min(len(feeds), (page + 1) * pagesize)]
        serializer = FeedSerializer(objs, many=True)
        return Response(serializer.data)


class RandomView(APIView):
    def post(self, request):
        print(request.data)
        return Response()


class CreateFeedView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser]

    def post(self, request):
        print(request.data)
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        obj = CreateFeedSerializer(context={"request": request}, data=request.data)
        print(obj)
        if obj.is_valid():
            obj.save()
            return Response()
        return Response({"message":"post is not created"})


class UpdateFeedView(APIView):
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser]

    def post(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "postid" not in request.data:
            return Response(status=status.HTTP_300_MULTIPLE_CHOICES)
        postid = request.data["postid"]
        myfeed = Feed.objects.filter(id=postid).first()
        if not myfeed:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        if myfeed.feeduser != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if "desc" in request.data:
            myfeed.desc = request.data["desc"]
        # if "avatar" in request.data:
        #     myfeed.avatar = request.data["avatar"]
        if "link" in request.data:
            myfeed.link = request.data["link"]
        myfeed.save()
        return Response()
