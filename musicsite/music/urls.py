from django.urls import path
from .views import MusicUpdateView, AlbumUpdateView, MusicCreateView, AlbumCreateView

app_name = 'music'

urlpatterns = [
    path('<pk>/music_update/', MusicUpdateView.as_view(), name='music_update'),
    path('<pk>/music_create/', MusicCreateView.as_view(), name='music_create'),
    path('<pk>/album_update/', AlbumUpdateView.as_view(), name='album_update'),
    path('<pk>/album_create/', AlbumCreateView.as_view(), name='album_create'),
]