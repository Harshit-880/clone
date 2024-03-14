from django.urls import path
from Profile.views import *

urlpatterns = [
    path('userprofile/',UserProfileView.as_view()),
    path('usermainprofile/<int:user_id>/',MainprofileView.as_view()),
    path('search/',ProfileSearchView.as_view()),
]

