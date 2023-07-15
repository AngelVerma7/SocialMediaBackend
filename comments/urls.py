from django.contrib import admin
from django.urls import path,include
from .views import * 


urlpatterns = [

    path('all',CommentByIdView.as_view()),
    path('add',AddCommentView.as_view()),


]
