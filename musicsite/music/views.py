from django.shortcuts import render, get_object_or_404
from accounts.models import User, UserProfile
from .models import Artist, Album
from django.views.generic import UpdateView, CreateView
from .forms import ArtistForm, AlbumForm
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
class MusicCreateView(CreateView):
    form_class = ArtistForm
    model = Artist
    template_name = 'music/music_create.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        profile = UserProfile.objects.get(user=self.request.user)
        form.instance.as_pro = profile
        return super().form_valid(form)

class AlbumCreateView(CreateView):
    form_class = AlbumForm
    model = Album
    template_name = 'music/album_create.html'
    success_url = reverse_lazy('accounts:profile')
    
    def form_valid(self, form):
        profile = UserProfile.objects.get(user=self.request.user)
        form.instance.as_pro = profile
        return super().form_valid(form)

class MusicUpdateView(UpdateView):
    form_class = ArtistForm
    model = Artist
    template_name = 'music/music_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, *args, **kwargs):
        pk =self.kwargs.get('pk')
        obj = Artist.objects.get(pk=pk)
        if not obj.as_pro.user == self.request.user:
            messages.warning(self.request, 'You need to be the associated profile to edit this')
        return obj

class AlbumUpdateView(UpdateView):
    form_class = AlbumForm
    model = Album
    template_name = 'music/album_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, *args, **kwargs):
        pk =self.kwargs.get('pk')
        obj = Album.objects.get(pk=pk)
        if not obj.as_pro.user == self.request.user:
            messages.warning(self.request, 'You need to be the associated profile to edit this')
        return obj

