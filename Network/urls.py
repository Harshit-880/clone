from django.urls import path
from Network.views import *

urlpatterns = [
    path('follow/',followview.as_view()),
    path('followersview/<int:user_id>/',followerView.as_view()),
]