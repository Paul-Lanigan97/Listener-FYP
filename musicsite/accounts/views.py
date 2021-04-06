from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login
from django.views.generic import DetailView, CreateView, UpdateView, ListView
from .models import UserProfile, Relationship
from django.views import generic
from django.urls import reverse_lazy
from .forms import EditProfileForm, EditPageForm
from django.contrib.auth.models import User
from django.db.models import Q
from music.models import Artist, Album

# Create your views here.

class EditPageView(generic.UpdateView):
    form_class = EditPageForm
    template_name = 'accounts/edit_page.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self):
        return self.request.user.userprofile


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('../profile/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            
            user = form.get_user()
            login(request, user)
            return redirect('posts:main-post-view')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    obj = Artist.objects.filter(as_pro=userprofile)
    obj2 = Album.objects.filter(as_pro=userprofile)


    context = {
        'userprofile': UserProfile,
        'obj' : Artist,
        'obj2' : Album,
    }
    
    return render(request, 'accounts/profile.html', context)

def invites_received_view(request):
    profile = UserProfile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    
    context = {
        'qs': results,
        'is_empty': is_empty,
        }

    return render(request, 'accounts/my_invites.html', context)

def accept_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = UserProfile.objects.get(pk=pk)
        receiver = UserProfile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('accounts:my_invites_view')

def reject_invitation(request):
    if request.method=="POST":
        pk = request.POST.get('profile_pk')
        sender = UserProfile.objects.get(pk=pk)
        receiver = UserProfile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('accounts:my_invites_view')


def profiles_list_view(request):
    user = request.user
    qs = UserProfile.objects.get_all_profiles(user)

    context = {'qs': qs}

    return render(request, 'accounts/profile_list.html', context)

def invite_profiles_list_view(request):
    user = request.user
    qs = UserProfile.objects.get_all_profiles_to_invite(user)

    context = {'qs': qs}

    return render(request, 'accounts/to_invite_list.html', context)

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'accounts/detail.html'

    #def get_object(self, slug = None):
        #slug = self.kwargs.get('slug')
        #profile = UserProfile.objects.get(slug=slug)
        #return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = UserProfile.objects.get(user=user)
        artists = Artist.objects.filter(as_pro=profile)
        album = Album.objects.filter(as_pro=profile)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['artists'] = artists
        context['album'] = album
        context['posts'] = self.get_object().get_all_authors_posts
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context


class ProfileListView(ListView):
    model = UserProfile
    template_name = 'accounts/profile_list.html'
    #context_object_name = 'qs'

    def get_queryset(self):
        qs = UserProfile.objects.get_all_profiles(self.request.user)
        return qs 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = UserProfile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

#def send_invitation(request):
    #if request.method=='POST':
        #pk = request.POST.get('profile_pk')
        #user = request.user
        #sender = UserProfile.objects.get(user=user)
        #receiver = UserProfile.objects.get(pk=pk)

        #rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        #return redirect(request.META.get('HTTP_REFERER'))
    #return redirect('accounts:profile')          

def remove_from_friends(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = UserProfile.objects.get(user=user)
        receiver = UserProfile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)) 
         )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('accounts:profile')

def send_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = UserProfile.objects.get(user=user)
        receiver = UserProfile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('accounts:profile')
