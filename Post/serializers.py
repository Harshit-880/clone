from rest_framework import serializers, status
from .models import *
from Post.models import *
from django.shortcuts import get_object_or_404
from Profile.serializers import ShortProfileSerializer



class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model=PostImages
        fields=['image']
 
class PostSerializer(serializers.ModelSerializer):

    images=serializers.ListField(child=serializers.ImageField(),write_only=True,required=False)
    post_owner_profile=ShortProfileSerializer(source="post_owner",read_only=True)

    class Meta:
        model=Post
        exclude = ['saved_by']

    def to_representation(self, instance):
        data= super().to_representation(instance)
        current_profile = get_object_or_404(Profile, user = self.context['request'].user)
        post_like=PostReaction.objects.filter(post=instance,reacted_by=current_profile)

        data['self_like']=False
        if post_like.exists():
            data['self_like']=True
        
        post_images=PostImages.objects.filter(post=instance)
        # to get only image from Post image model we use PostImageSerializer 
        data['image']=PostImageSerializer(instance=post_images,many=True).data
        data['created_at']=instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['like_count'] = len(data.pop('reacted_by'))
        # reacted_by data is in the same model Post
        data['reacted_by'] = ShortProfileSerializer(instance=instance.reacted_by,many=True).data[:2]
        
        post_comments=Comment.objects.filter(post=instance)
        # replies_count=0
        # for post_comment in post_comments:
        #     replies_count+= post_comment.commentReply

        return data



    
    def create(self, validated_data):
        
        try: 
            images=validated_data.pop('images')
        except KeyError:
            images=[]
        post=super().create(validated_data)

        post_images_list=[]
        for image in images:
            post_images_list.append(
                PostImages(post=post,image=image)
                )
        if post_images_list: 
            PostImages.objects.bulk_create(post_images_list)
        return post
        