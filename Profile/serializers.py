from rest_framework import serializers, status
from .models import Profile
from account.utils import CustomValidation
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


# serializer to edit or update the profile
class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Profile
        exclude=['id','follower']

    # def update(self, instance, validated_data):
    #     try:
    #         username=validated_data.get('username')
    #     except KeyError:
    #         return super().update(instance,validated_data)
    #     if Profile.objects.filter(username=username).exclude(id=instance.id).exist():
    #         raise CustomValidation(detail='this username is taken',
    #                                field='username',
    #                                status_code=status.HTTP_409_CONFLICT)
    #     # valid_username= username.replace(" ","")
    #     # if username != valid_username:
    #     #     raise CustomValidation(detail='this username is not in correct formate',
    #     #                            field='username',
    #     #                            status_code=status.HTTP_400_BAD_REQUEST)
    #     validated_data['username']=username.lower()
    #     return super().update(instance, validated_data)
        

    def update(self, instance, validated_data):
        username = validated_data.get('username', instance.username)

        # Check if the new username is unique (excluding the current instance)
        if Profile.objects.filter(username=username).exclude(id=instance.id).exists():
            raise ValidationError({'username': 'This username is already taken.'})
        # instance.name = validated_data.get('name', instance.name)
        # instance.username = username
        # instance.bio = validated_data.get('bio', instance.bio)
        # # Add any other fields you want to update

        # # Save the updated instance
        # instance.save()
        # return instance
        image=validated_data.get('image', None)
        if image :
            # If a new image is provided, delete the existing image
            if instance.profile_image:
                instance.profile_image.delete()
            instance.profile_image=image
        valid_username = username.replace(" ", "")
        if username != valid_username:
            raise CustomValidation(detail ='This username has wrong format',
                                   field = 'username',
                                   status_code= status.HTTP_400_BAD_REQUEST)
        validated_data['username']= username.lower()
        return super().update(instance, validated_data)
    

class ShortProfileSerializer(serializers.ModelSerializer):
        
    class Meta:
            model=Profile
            fields=['username','profile_image','id']

    def to_representation(self, instance):
            return super().to_representation(instance)



class MainProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=Profile
        exclude=['id']

    # def get_follower(self, obj):
    #     return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['followers_count'] = len(instance.follower.all())
        data['following_count'] = len(instance.user.following.all())
        return data
    


# class ProfileSearchSerializer(serializers.ModelSerializer):

#     class Meta:
#         model=Profile
