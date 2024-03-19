from django.shortcuts import render
from rest_framework import status
from Post.serializers import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from .models import *
from Profile.models import Profile
from rest_framework.generics import CreateAPIView,ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response




class PostUplode(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class=PostSerializer

    def post(self,request,*args,**kwargs):

        request.data.update({"post_owner" : Profile.objects.get(user=request.user).id})
        return super().post(request,*args,**kwargs)
    

class likeUplode(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class=LikeSerializer
    
    def post(self, request, format=None):
        # Only post ID is required in the request data
        data = {'post': request.data.get('post')}
        serializer = LikeSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)