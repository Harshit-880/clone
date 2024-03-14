from django.urls import path
from Post.views import PostUplode

urlpatterns = [
    path('uplode/',PostUplode.as_view()),
    
]