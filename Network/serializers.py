from rest_framework import serializers, status
from .models import *
from Profile.serializers import ShortProfileSerializer
from Profile.models import *
from django.shortcuts import get_object_or_404
from Profile.models import Profile


class followRequeserializer(serializers.ModelSerializer):

    profile_id=serializers.IntegerField()

    class Meta:
        model = Profile
        fields = ['profile_id']

# class followerSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model=Follow
#         exclude=['id','profile']

#     def to_representation(self, instance):
#         data= super().to_representation(instance)
#         # my_data=instance.followers_set.id
#         # data['followed_by'] = ShortProfileSerializer(instance=my_data,many=True)
#         # profiledata=ShortProfileSerializer(instance,many=True)
#         # data['follower_profiles']=profiledata
        
#         # my_data=list(instance.followers_set.id)
#         # print(my_data)
#         # serialized_profiles = ShortProfileSerializer(my_data,many=True).data
#         # data['followed_by'] = serialized_profiles

#         return data
        

class FollowersSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Follow
        exclude=['id','profile']
        # this function serialize the queryset come from view in iterative way the output is below
        # OrderedDict([('followers_set', 3)])
        # root3@gmail.com --> root3-->3
        # OrderedDict([('followers_set', 2)])
        # root1@gmail.com --> root1-->2
    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(data)
        follower_profile = get_object_or_404(Profile,user = data['followers_set'] )
        print(follower_profile)
        data['follower_profile_data'] = ShortProfileSerializer(instance = follower_profile, many = False).data
        return data


class FollowingSerializer(serializers.ModelSerializer):
    
    following_profile_data = ShortProfileSerializer(source = "profile", read_only = True)
    # By defining following_profile_data above the model declaration,
    # the serializer can include this field in its serialization output along with the other data of the follow model
    class Meta:
        model = Follow
        exclude=['id','profile','followers_set']
        