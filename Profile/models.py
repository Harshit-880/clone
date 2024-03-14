from django.db import models
from account.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=100, blank = True, null = True)
    bio = models.TextField(blank = True, null = True, default=None)
    follower = models.ManyToManyField(User, through='Network.Follow',related_name="following", blank=True)
    profile_image=models.ImageField(upload_to="my_picture",blank=True)
    
    # following = models.ManyToManyField(User, through='Network.Follow',related_name="followers", blank=True)


    def __str__(self):
        return f"{self.user} --> {self.name}-->{self.id}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance , name= instance.name)