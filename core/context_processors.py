from profiles.models import Organizer 

def organizer_profile_exists(request):
    if request.user.is_authenticated:
        return {
            'has_organizer_profile': Organizer.objects.filter(user=request.user).exists()
        }
    return {'has_organizer_profile': False}