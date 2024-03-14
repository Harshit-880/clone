from django.shortcuts import render
from rest_framework import status
from Post.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import *
from rest_framework.generics import CreateAPIView




class PostUplode(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class=PostSerializer

    def post(self,request,*args,**kwargs):

        request.data.update({"post_owner" : Profile.objects.get(user=request.user).id})
        return super().post(request,*args,**kwargs)