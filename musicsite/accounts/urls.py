from django.urls import path
from . import views
from .views import (
    UserEditView, 
    profile, 
    EditPageView, 
    invites_received_view, 
    profiles_list_view, 
    invite_profiles_list_view, 
    ProfileDetailView,
    ProfileListView,
    send_invitation,
    remove_from_friends,
    accept_invitation,
    reject_invitation
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name = "signup"),
    path('login/', views.login_view, name = "login"),
    path('profile/', views.profile, name = "profile"),
    path('edit_profile/', UserEditView.as_view(), name = 'edit_profile'),
    path('edit_page/', EditPageView.as_view(), name = 'edit_page'),
    path('my_invites/', invites_received_view, name = 'my_invites_view'),
    path('all_profiles/', ProfileListView.as_view(), name = 'all_profiles_view'),
    path('<slug>/', ProfileDetailView.as_view(), name="profile-detail-view"),
    path('to_invite/', invite_profiles_list_view, name = 'invite_profiles_view'),
    path('send_invite/', send_invitation, name='send_invite'),
    path('remove_friend/', remove_from_friends, name='remove_friend'),
    path('my_invites/accept/', accept_invitation, name='accept_invite'),
    path('my_invites/reject/', reject_invitation, name='reject_invite')
]