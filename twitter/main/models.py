from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Auth(models.Model):
    image = models.ImageField(upload_to="img")
    born_date = models.DateField()
    location = models.CharField(max_length=25)
    tweets = models.CharField(max_length=140)
    Biography = models.ForeignKey('Biography')
    user = models.OneToOneField('auth.User')


class Tweet(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.TextField(max_length=150)
    auth = models.ForeignKey('Auth')


class Biography(models.Model):
    age = models.CharField(max_length=2)
    about_me = models.TextField(max_length=150)


class Users(models.Model):
    user = models.OneToOneField(User)
    birthday = models.DateField()
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

#def create_user(sender, instance, **kwargs):
#    users, new = User.objects.get_or_create(user=instance)
#post_save.connect(create_user, User)