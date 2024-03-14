from django.contrib import admin
from .models import *

# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'name', 'username', 'bio', 'profile_image', 'display_followers')

#     def display_followers(self, obj):
#         return ", ".join([follower_user.name for follower_user in obj.follower.all()])

#     display_followers.short_description = 'Followers'

# admin.site.register(Profile, ProfileAdmin)

admin.site.register(Profile)