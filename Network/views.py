from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import followRequeserializer,followerSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import *
from Profile.models import Profile
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

# Create your views here.

class followview(APIView):

    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):

        serializer=followRequeserializer(data=request.data)
        if serializer.is_valid():
            follower=self.request.user
        
            profile_id=serializer.validated_data['profile_id']
            profile_user=get_object_or_404(User,id=profile_id)
            if( profile_user==follower):
                return Response({"message": "can not follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(profile=profile_user.profile,followers_set=follower)

            return Response({"message": "Follow relationship created successfully."}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class followerView(ListAPIView):

    permission_classes=[IsAuthenticated]
    serializer_class=followerSerializer

    def get(self, request,user_id, *args, **kwargs):
        if user_id is None:
            return Response({'error': 'requested_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_profile=get_object_or_404(Profile,user=user_id)
            profiles=Follow.objects.filter(profile=user_profile)
            serializer=followerSerializer(profiles)
            return Response(serializer.data , status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"detail": "No Profile exists with this username"}, status=status.HTTP_400_BAD_REQUEST)
         