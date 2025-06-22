from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from profiles.models import Organizer
from events.models import Event
from django.utils.dateparse import parse_datetime

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            organizer = Organizer.objects.get(user=request.user)
            event.organizer = organizer
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()

    return render(request, 'create-event.html', {'form': form})

def event_list(request):
    events = Event.objects.all().order_by('-start_time')
    return render(request, 'events.html', {'events': events})

def event_details(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    return render(request, 'details-event.html', {'event': event})

def event_edit(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    
    if request.method == 'POST':
        slogan = request.POST.get('slogan', '').strip()
        location = request.POST.get('location', '').strip()
        start_time_str = request.POST.get('start_time')
        available_tickets = request.POST.get('available_tickets')
        key_features = request.POST.get('key_features', '').strip()
        banner_url = request.POST.get('banner_url', '').strip()
        
        errors = {}

        # Validation
        if not slogan:
            errors['slogan'] = 'Slogan is required.'
        if not location:
            errors['location'] = 'Location is required.'

        # Parse start_time
        if start_time_str:
            # datetime-local input sends in format 'YYYY-MM-DDTHH:MM'
            start_time = parse_datetime(start_time_str)
            if start_time is None:
                errors['start_time'] = 'Invalid date/time format.'
        else:
            errors['start_time'] = 'Start time is required.'

        try:
            available_tickets = int(available_tickets)
            if available_tickets < 0:
                errors['available_tickets'] = 'Available tickets must be zero or more.'
        except (ValueError, TypeError):
            errors['available_tickets'] = 'Available tickets must be a number.'

        if banner_url and len(banner_url) > 200:
            errors['banner_url'] = 'Banner URL must be 200 characters or less.'

        # If no errors, update and redirect
        if not errors:
            event.slogan = slogan
            event.location = location
            event.start_time = start_time
            event.available_tickets = available_tickets
            event.key_features = key_features
            event.banner_url = banner_url if banner_url else None
            event.save()
            return redirect('event-details', event_pk=event.pk)

        # On errors, re-render the form with error messages and previously entered data
        context = {
            'event': event,
            'errors': errors,
            # Also you can pass the posted values here if you want to override the event's values in template
            'posted': request.POST,
        }
        return render(request, 'edit-event.html', context)

    # GET request
    return render(request, 'edit-event.html', {'event': event})

def event_delete(request, event_pk):
    event = get_object_or_404(Event, pk=event_pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list') 
    return render(request, 'delete-event.html', {'event': event})