from rest_framework import serializers, status
from .models import *
from Profile.serializers import ShortProfileSerializer
from Profile.models import *
from django.shortcuts import get_object_or_404


class followRequeserializer(serializers.ModelSerializer):

    profile_id=serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ['profile_id']

class followerSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=Follow
        fields = "__all__"

    def to_representation(self, instance):
        data= super().to_representation(instance)
        print(instance)
        # follower_profile = data[1]
        # print(follower_profile)
        # data['follower']=ShortProfileSerializer(instance = follower_profile, many = False).data
        return data
        
