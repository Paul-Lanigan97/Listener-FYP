from .models import UserProfile, Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = UserProfile.objects.get(user=request.user)
        pic = profile_obj.profile_img
        return{'picture':pic}
    return{}

def invitations_received_no(request):
    if request.user.is_authenticated:
        profile_obj = UserProfile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count
        return{'invites_num':qs_count}
    return {}