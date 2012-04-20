from django.db import models


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
