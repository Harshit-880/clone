from django.db import models
from Profile.models import Profile
from django.utils import timezone

class Post(models.Model):
    post_owner=models.ForeignKey(Profile,related_name="created_post",on_delete=models.CASCADE)
    text=models.TextField()
    saved_by = models.ManyToManyField(Profile, related_name="saved_posts", blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    reacted_by = models.ManyToManyField(Profile, through='PostReaction', related_name="reacted_posts")
    commented_by = models.ManyToManyField(Profile, through='Comment', related_name="commented_posts")
    
    def __str__(self):
        return f"{self.post_owner.full_name}--> Post{self.id}"


class PostImages(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/images/')

class PostReaction(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    reacted_by=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="post_reaction")

class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_owner=models.ForeignKey(Profile,on_delete=models.CASCADE)
    text=models.TextField()
    replied_by = models.ManyToManyField(Profile, through='CommentReply',related_name = "replied_comments")
    created_at = models.DateTimeField(default=timezone.now)

class commentReply(models.Model):
    comment=models.ForeignKey(Comment, on_delete=models.CASCADE)
    reply_owner=models.ForeignKey(Profile, on_delete=models.CASCADE)
    text=models.TextField()
    created_at = models.DateTimeField(default=timezone.now)



class HashTag(models.Model):
    
    topic = models.CharField(max_length = 255)
    associated_posts = models.ManyToManyField(Post, related_name = "hashtags", blank = True)
    followed_by = models.ManyToManyField(Profile,  related_name = "followed_hastags")
    