from django.contrib import admin
from main.models import UserProfile, Tweet


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'biography',)


class TweetAdmin(admin.ModelAdmin):
    list_display = ('auth', 'status', 'created_at',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Tweet, TweetAdmin)
