from django.urls import path
from Post.views import PostUplode,likeUplode,CommentUplodeview

urlpatterns = [
    path('uplode/',PostUplode.as_view()),
    path('likeUplode/',likeUplode.as_view()),
    path('CommentUplodeview/',CommentUplodeview.as_view()),
]