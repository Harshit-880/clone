from django.db import models
from account.models import User

CONNECTION_STATES = [
        ('Pending', 'Pending'),
        ('Withdrawn', 'Withdrawn'),
        ('Ignored', 'Ignored')
    ]


class ConnectionRequest(models.Model):
    sender=models.ForeignKey("Profile.Profile",on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey("Profile.Profile", on_delete=models.CASCADE, related_name = "reciever")
    state = models.CharField(max_length=255, choices=CONNECTION_STATES, default="Pending")
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('sender', 'reciever'))


class Follow(models.Model):
    
    profile = models.ForeignKey("Profile.Profile", on_delete=models.CASCADE)
    followers_set = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    class Meta:
        unique_together = ('profile','followers_set')
