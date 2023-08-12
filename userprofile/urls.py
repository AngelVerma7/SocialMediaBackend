from django.contrib import admin
from django.urls import path,include
from .views import * 


urlpatterns = [
    # path('',ProfileView.as_view()),
    path('search',SearchUserView.as_view()),
    path('searchall',SearchPageUserView.as_view()),
    path('update',UpdateProfile.as_view()),
    path('userfeeds',UserFeeds.as_view()),
    path('userprofile',ProfileView.as_view()),
    path('<str:username>',ProfileView.as_view()),


]
