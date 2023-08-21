from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.parsers import MultiPartParser

from .models import *
from .serializers import *
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.tokens import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from userLogin.serializers import *
from feeds.models import * 
from feeds.serializers import * 


class SearchUserView(APIView):
    def post(self,request):
        searchKey=""
        if "username" in request.data:
            searchKey=request.data["username"]
        else:
            return Response()
        if searchKey=="":
            return Response([])
        
        matched=User.objects.filter(username__contains=searchKey)
        print(matched)
        if len(matched)>5:
            matched=matched[:5]
        st=set()
        for i in matched:
            st.add(i.id)
        res=UserProfile.objects.filter(profileuser__in=st)
        serializer=UserProfileSerializer(res,many=True)
        
        return Response(serializer.data)
    
class SearchPageUserView(APIView):
    def post(self,request):
        searchKey=""
        if "username" in request.data :
            searchKey=request.data["username"]
        else:
            return Response()
        page=0
        if "page" in request.data:
            page=request.data["page"]
        if searchKey=="":
            return Response([])
        
        matched=User.objects.filter(username__contains=searchKey)
        pagesize=4
        maxpage = int(len(matched) / pagesize + (1 if len(matched) % pagesize else 0))
        if(page >=maxpage):
            return Response({"remaining feeds are":0,"feeds":[]})
        page = int(page % maxpage)
        objs = matched[(page) * pagesize : min(len(matched), (page + 1) * pagesize)]
        st=set()
        for i in objs:
            st.add(i.id)
        res=UserProfile.objects.filter(profileuser__in=st)
        serializer=UserProfileSerializer(res,many=True)
        res=dict()
        if page==maxpage-1:
            res["remaining"]=0
        else:
            res["remaining"]=1
        res["pages"]=maxpage
        res["feeds"]=serializer.data    
        return Response(res)
    


    
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
            userData=UserProfileSerializer(userobj,context={"request":request}) 
            return Response(userData.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

class UpdateProfile(APIView):
    parser_classes=[MultiPartParser]
    authentication_classes=[JWTAuthentication]
    serializer_class=ProfileUpdateSerializer
    def post(self,request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
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
        if "username" not in request.data : 
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        page=0
        if "page" in request.data:
            page=request.data["page"]
        pagesize=10
        user=User.objects.filter(username=request.data["username"]).first()
        
        if not user:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        profile=UserProfile.objects.filter(profileuser=user).first()
        if not profile:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        feeds=Feed.objects.filter(feeduser=profile).order_by("-edited")
            #    feeds = Feed.objects.all()
        maxpage = int((len(feeds) / pagesize )+ (1 if len(feeds) % pagesize else 0))
        print("the maxpage is",maxpage)
        print("the page is",page)
        if(page >=maxpage):
            return Response({"remaining feeds are":0,"feeds":[]})
        page = int(page % maxpage)
        objs = feeds[(page) * pagesize : min(len(feeds), (page + 1) * pagesize)]
        serializer = FeedSerializer(objs, many=True)
        res=dict()
        if page==maxpage-1:
            res["remaining"]=0
        else:
            res["remaining"]=1
        res["feeds"]=serializer.data    
        return Response(res)
            

        # feeds=Feed.objects.filter(feeduser=request.data["username"])
        data=FeedSerializer(feeds,many=True)

        return Response(data.data)  

