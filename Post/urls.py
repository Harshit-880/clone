from django.urls import path
from Post.views import PostUplode,likeUplode

urlpatterns = [
    path('uplode/',PostUplode.as_view()),
    path('likeUplode/',likeUplode.as_view()),
]