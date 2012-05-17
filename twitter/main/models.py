from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(max_length=150)
    auth = models.ForeignKey('UserProfile')

    def __unicode__(self):
        return '%s' % self.status


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    followin = models.ManyToManyField('UserProfile', blank=True)
    image = models.ImageField(upload_to="main/static/img", blank=True)
    birthday = models.DateField(auto_now=True)
    location = models.CharField(max_length=25)
    biography = models.TextField(max_length=150)

    def __unicode__(self):
        return '%s' % self.user.username

    def get_biography(self):
        return self.biography


def get_profile(user):
        if not hasattr(user, '_profile_cache'):
            profile, created = UserProfile.objects.get_or_create(user=user)
        return profile
User.get_profile = get_profile
