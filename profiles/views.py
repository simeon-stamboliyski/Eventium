from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import OrganizerForm
from django.contrib.auth import authenticate, login
from profiles.models import Organizer
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def profile_create(request):
    if request.method == 'POST':
        form = OrganizerForm(request.POST)
        if form.is_valid():
            organizer = form.save() 
            
            user = authenticate(
                request, 
                username=organizer.company_name, 
                password=form.cleaned_data['secret_key']
            )
            if user is not None:
                login(request, user)
            
            return redirect('event_list')
    else:
        form = OrganizerForm()

    return render(request, 'create-organizer.html', {'form': form})

@login_required
def profile_details(request):
    organizer = get_object_or_404(Organizer, user=request.user)

    upcoming_events = organizer.events.filter(start_time__gt=now()).order_by('start_time')

    context = {
        'organizer': organizer,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'details-organizer.html', context)

def profile_edit(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        website = request.POST.get('website', '').strip()

        errors = {}

        # Validate company_name with your model validator
        try:
            Organizer._meta.get_field('company_name').run_validators(company_name)
        except ValidationError as e:
            errors['company_name'] = e.messages

        # Validate phone_number
        try:
            Organizer._meta.get_field('phone_number').run_validators(phone_number)
        except ValidationError as e:
            errors['phone_number'] = e.messages

        # website is optional; if provided, validate URLField
        if website:
            try:
                Organizer._meta.get_field('website').run_validators(website)
            except ValidationError as e:
                errors['website'] = e.messages
        else:
            website = None

        # Check unique constraints manually because update won't auto-check them
        if Organizer.objects.exclude(pk=organizer.pk).filter(company_name=company_name).exists():
            errors.setdefault('company_name', []).append("Company name already exists!")

        if Organizer.objects.exclude(pk=organizer.pk).filter(phone_number=phone_number).exists():
            errors.setdefault('phone_number', []).append("Phone number already in use!")

        if errors:
            # Render form again with errors and current submitted values
            organizer.company_name = company_name
            organizer.phone_number = phone_number
            organizer.website = website

            return render(request, 'edit-organizer.html', {
                'organizer': organizer,
                'errors': errors,
            })

        # If no errors, save
        organizer.company_name = company_name
        organizer.phone_number = phone_number
        organizer.website = website
        organizer.save()

        # Redirect to organizer detail/profile page after success
        return redirect('profile-details')

    else:
        # GET request - show form with existing organizer data
        return render(request, 'edit-organizer.html', {
            'organizer': organizer,
            'errors': {},
        })

def profile_delete(request, pk):
    from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from profiles.models import Organizer

def profile_delete(request, pk):
    organizer = get_object_or_404(Organizer, pk=pk)
    user = organizer.user 

    if request.method == 'POST':
        now = timezone.now()
        upcoming_events = organizer.events.filter(start_time__gte=now)

        if upcoming_events.exists():
            messages.error(request, "Cannot delete profile: You have upcoming events.")
            return redirect('index')  

        organizer.delete()
        user.delete()

        messages.success(request, "Your organizer profile has been deleted.")
        return redirect('index')

    return render(request, 'delete-organizer.html', {'organizer': organizer})