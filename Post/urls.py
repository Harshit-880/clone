from django.urls import path
from Post.views import PostUplode,likeUplode,CommentUplodeview,ReplyUplodeview

urlpatterns = [
    path('uplode/',PostUplode.as_view()),
    path('likeUplode/',likeUplode.as_view()),
    path('CommentUplodeview/',CommentUplodeview.as_view()),
    path('ReplyUplodeview/',ReplyUplodeview.as_view()),
]