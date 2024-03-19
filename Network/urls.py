from django.urls import path
from Network.views import *

urlpatterns = [
    path('follow/',followview.as_view()),
    path('followersview/<int:user_id>/',FollowersView.as_view()),
    path('followingview/<int:user_id>/',FollowingView.as_view()),
]