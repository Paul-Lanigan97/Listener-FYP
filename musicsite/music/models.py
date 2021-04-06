from django.db import models
from accounts.models import UserProfile
from django.core.validators import FileExtensionValidator

# Create your models here.
class Artist(models.Model):
    artist_name = models.CharField(default='', max_length=200)
    artist_name2 = models.CharField(default='', max_length=200)
    artist_name3 = models.CharField(default='', max_length=200)
    artist_name4 = models.CharField(default='', max_length=200)
    artist_name5 = models.CharField(default='', max_length=200)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    as_pro = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='artist')


    def __str__(self):
        return f"{self.as_pro}-{'Artist List'}"


class Album(models.Model):
    album_artist = models.CharField(default='', max_length=200)
    album_name = models.CharField(default='', max_length=200)
    genre = models.CharField(default='', max_length=200, null=True)
    album_art = models.ImageField(upload_to='images', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    as_pro = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='album')

    def __str__(self):
        return f"{self.as_pro}-{'Album List'}"