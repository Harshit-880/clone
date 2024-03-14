from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.generics import *
from Profile.serializers import ProfileSerializer,MainProfileSerializer,ShortProfileSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
# Create your views here.



class UserProfileView(CreateAPIView,RetrieveAPIView):
    
    permission_classes=[IsAuthenticated]
    serializer_class= ProfileSerializer

    def get_object(self):
        return get_object_or_404(Profile,user=self.request.user)
    
    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            # used to print the error in the consol
            print("hello")      
            import traceback
            traceback.print_exc()
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def perform_update(self, serializer):
        serializer.save()



class MainprofileView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = MainProfileSerializer
    

    def get(self, request,user_id, *args, **kwargs):
        authenticated_user_id = request.user.id
        # requested_user_id = request.get('id')
        requested_user_id=user_id
        # print(authenticated_user_id)
        # print(requested_user_id)

        if requested_user_id is None:
            return Response({'error': 'requested_user_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(id=requested_user_id)
            serializer = MainProfileSerializer(profile)
            if authenticated_user_id == profile.user.id:
               
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data , status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)   
        


class ProfileSearchView(ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ShortProfileSerializer

    queryset=Profile.objects.all()
    filter_backends=[filters.SearchFilter]
    search_fields=['username','name']