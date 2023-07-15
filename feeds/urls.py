from django.contrib import admin
from django.urls import path,include
from .views import * 


urlpatterns = [
    path('like',LikeFeedView.as_view()),
    path('unlike',UnlikeFeedView.as_view()),
    path('myfeed',MyFeedView.as_view()),
    path('createfeed',CreateFeedView.as_view()),
    path('update',UpdateFeedView.as_view()),
    path('delete',DeleteFeedView.as_view()),
    path('page',FeedPagesView.as_view()),
    path('id/<str:postid>',FeedView.as_view()),
    path('random',RandomView.as_view()),
    
    # path('<str:username>',ProfileView.as_view()),
    # path('update',UpdateProfile.as_view()),


]
