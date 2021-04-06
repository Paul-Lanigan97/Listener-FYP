from django import forms
from .models import Artist, Album

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('artist_name', 'artist_name2', 'artist_name3', 'artist_name4','artist_name5')

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('album_artist', 'album_name', 'genre', 'album_art')



