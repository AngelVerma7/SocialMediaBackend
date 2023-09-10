from django.contrib import admin
from django.urls import path,include
from .views import * 


urlpatterns = [
    path('startFollowing',StartFollowingView.as_view()),
    path('unfollow',UnfollowView.as_view()),
    path('findDegree',FollowDegreeView.as_view()),
    path('recentfollowers',RecentFollowersView.as_view()),
    path('recentfollowings',RecentFollowingsView.as_view()),
  


]
