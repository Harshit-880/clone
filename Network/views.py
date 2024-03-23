from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import followRequeserializer,FollowersSerializer,FollowingSerializer
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
            print(follower)# return email
            profile_id=serializer.validated_data['profile_id']
            profile_user=get_object_or_404(User,id=profile_id)
            if( profile_user==follower):
                return Response({"message": "can not follow yourself"}, status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.create(profile=profile_user.profile,followers_set=follower)

            return Response({"message": "Follow relationship created successfully."}, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class followerView(ListAPIView):

#     permission_classes=[IsAuthenticated]
#     serializer_class=followerSerializer

#     def get(self, request,user_id, *args, **kwargs):
#         if user_id is None:
#             return Response({'error': 'requested_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user_profile=get_object_or_404(Profile,user=user_id)
#             profiles=Follow.objects.filter(profile=user_profile)
#             follow_instances = list(profiles)
#             print(follow_instances)
#             serializer = followerSerializer('json', follow_instances)
#             serializer.is_valid()
#             return Response(serializer.data , status=status.HTTP_200_OK)
#         except ObjectDoesNotExist:
#             return Response({"detail": "No Profile exists with this username"}, status=status.HTTP_400_BAD_REQUEST)
         

class FollowersView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = FollowersSerializer
    
    def get_queryset(self):# this function return queryset
        user_id = self.kwargs.get('user_id')
        print(user_id)
        if not user_id:
            raise ValidationError("User profile not found for the given user_id")
        user_profile = get_object_or_404(Profile, user = user_id)
        return Follow.objects.filter(profile = user_profile)
        # After obtaining the queryset from the get_queryset method,
        #  the next step in the Django REST Framework's request-response cycle 
        # involves serialization. The serializer class specified in your view's 
        # serializer_class attribute is responsible for converting the queryset 
        # (or individual objects) into a JSON format (or other specified format 
        #  if you're using a different serializer).
        

class FollowingView(ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = FollowingSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Follow.objects.filter(followers_set = user_id)
    

class UnfollowView(views.APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        
        id = request.data.get('id')
        if id is None:
            return Response({"detail": "Please provide the username."}, status=status.HTTP_400_BAD_REQUEST)
        
        profile = get_object_or_404(Profile, id=id)
        if not profile.follower.filter(id = self.request.user.id).exists():
            return Response({"detail": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)



        profile.follower.remove(self.request.user)
        return Response({"detail": "You have successfully unfollowed the user"}, status=status.HTTP_200_OK)