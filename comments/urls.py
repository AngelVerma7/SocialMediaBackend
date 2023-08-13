from django.contrib import admin
from django.urls import path,include
from .views import * 


urlpatterns = [

    path('all',CommentByIdView.as_view()),
    path('add',AddCommentView.as_view()),
    path('addreply',AddCommentReplyView.as_view()),
    path('getreply',CommentReplyView.as_view()),
    path('deletereply',DeleteCommentReplyView.as_view()),
    path('likeComment',LikeCommentView.as_view()),
    path('unlikeComment',UnlikeCommentView.as_view()),


]
