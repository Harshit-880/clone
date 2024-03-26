from rest_framework import serializers, status
from .models import *
from Post.models import *
from rest_framework.exceptions import ValidationError
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
        # print(instance)
        # to get only image from Post image model we use PostImageSerializer 
        data['image']=PostImageSerializer(instance=post_images,many=True).data
        data['created_at']=instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['like_count'] = len(data.pop('reacted_by'))
        # reacted_by data is in the same model Post
        # print(instance.reacted_by)
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
        

class LikeSerializer(serializers.ModelSerializer):

    # reacted_by_profile = ShortProfileSerializer(source = "reacted_by",read_only = True)
    # post_data = PostSerializer(source = "post", read_only = True)

    class Meta:
        model= PostReaction
        fields=['post']

    def create(self, validated_data):
        post=validated_data.get('post')
        reacted_by = self.context['request'].user.profile
        existing_reaction = PostReaction.objects.filter(post=post, reacted_by=reacted_by).exists()
        if existing_reaction:
            raise ValidationError("You've already reacted to this post.")
        return super().create(validated_data)
    

class CommentUplodeSerializer(serializers.ModelSerializer):

    comment_owner_profile = ShortProfileSerializer(source = "comment_owner",read_only = True)

    class Meta:
        model=Comment
        fields='__all__'

    def to_representation(self, instance):
        data=super().to_representation(instance)
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        data['replies_count'] = len(data.pop('replied_by'))
        return data

    def create(self, validated_data):
        comment=super().create(validated_data)
        return comment
    
class ReplyUplodeSerializer(serializers.ModelSerializer):

    reply_owner_profile = ShortProfileSerializer(source = "reply_owner",read_only = True)
    class Meta:
        model=commentReply
        fields="__all__"
    
    def to_representation(self, instance):
        data= super().to_representation(instance)
        data['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return data
    
    def create(self, validated_data):
        reply = super().create(validated_data)
        return reply