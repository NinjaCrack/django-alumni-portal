from django.shortcuts import get_object_or_404, render, redirect
from .models import Event
from authentication.models import User
import requests
from django.utils.timezone import now
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from django.urls import reverse
from faculty.models import WebsiteSettings
from alumniwebsite.forms import FormWithCaptcha

def events(request):
    websettings = WebsiteSettings.objects.first()

    current_year = now().year
    years = list(range(2010, current_year + 1))

    latest_events = Event.objects.filter(is_active=True).order_by('-date')[:3]

    months = [
        {'value': 0, 'name': 'All'},
        {'value': 1, 'name': 'January'},
        {'value': 2, 'name': 'February'},
        {'value': 3, 'name': 'March'},
        {'value': 4, 'name': 'April'},
        {'value': 5, 'name': 'May'},
        {'value': 6, 'name': 'June'},
        {'value': 7, 'name': 'July'},
        {'value': 8, 'name': 'August'},
        {'value': 9, 'name': 'September'},
        {'value': 10, 'name': 'October'},
        {'value': 11, 'name': 'November'},
        {'value': 12, 'name': 'December'}
    ]

    return render(request, 'events/events_list.html', {
        'years': years,
        'months': months,
        'current_year': current_year,
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
        'latest_events': latest_events,
    })

def user_events(request):
    access_token = request.COOKIES.get('access_token')
    
    if not access_token:
        return JsonResponse({"events": []})

    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
    user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
    
    if user_response.status_code != 200:
        return JsonResponse({"events": []})  # Return an empty array if request fails

    user_data = user_response.json()
    userevents = user_data.get('events', [])  # Ensure it's an array

    return JsonResponse({"events": userevents}) 

def event_page(request, slug):
    event = get_object_or_404(Event, slug=slug, is_active=True)
    access_token = request.COOKIES.get('access_token')
    websettings = WebsiteSettings.objects.first()
    is_authenticated = False
    user_events = None

    if access_token:
        # Verify token
        verify_url = f"{settings.API_TOKEN_URL}/token/verify/"
        verify_data = {'token': access_token}

        try:
            verify_response = requests.post(verify_url, data=verify_data)
            if verify_response.status_code == 200:
                is_authenticated = True

                # If token is valid, fetch user info
                user_info_url = f"{settings.API_TOKEN_URL}/user_info/"
                user_response = requests.get(
                    user_info_url,
                    headers={'Authorization': f'Bearer {access_token}'}
                )

                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user_events = user_data.get('events')
        except requests.RequestException:
            pass  # Optionally log the error here

    context = {
        'event': event,
        'form' : FormWithCaptcha(),
        "RECAPTCHA_PUBLIC_KEY": settings.RECAPTCHA_PUBLIC_KEY,
        'settings': websettings,
        'is_authenticated': is_authenticated,
        'user_events': user_events
    }
    return render(request, 'events/event_page.html', context)

def signup_event(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'events/signup_page.html', {'event': event})

def save_event(request, id):

    # Get access token from cookies
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized

    # Fetch user information
    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
    try:
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
        if user_response.status_code != 200:
            return JsonResponse({"error": "Failed to authenticate user"}, status=403)  # Forbidden

        user_data = user_response.json()
        user_email = user_data.get('email')
        if not user_email:
            return JsonResponse({"error": "Invalid user data received"}, status=400)  # Bad Request

    except requests.RequestException:
        return JsonResponse({"error": "Error contacting user API"}, status=500)  # Internal Server Error

    try:
        user = User.objects.get(email=user_email)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)  # Not Found
    
    if any(event["id"] == id for event in user.events):
        return JsonResponse({"message": "Event already saved"}, status=200)

    user.events.append({"id": id, "saved_at": now().isoformat()})

    try:
        user.save()
        return JsonResponse({"message": "Event saved successfully"}, status=201)
    except Exception as e:
        return JsonResponse({"error": f"Error saving event: {str(e)}"}, status=500)
    

def unsave_event(request, id):

    access_token = request.COOKIES.get('access_token')
    if not access_token:
        return JsonResponse({"error": "Access token is missing"}, status=401)  # Unauthorized


    user_api_url = f"{settings.API_TOKEN_URL}/user_info/"
    try:
        user_response = requests.get(user_api_url, headers={'Authorization': f'Bearer {access_token}'})
        if user_response.status_code != 200:
            return JsonResponse({"error": "Failed to authenticate user"}, status=403)  # Forbidden

        user_data = user_response.json()
        user_email = user_data.get('email')
        if not user_email:
            return JsonResponse({"error": "Invalid user data received"}, status=400)  # Bad Request

    except requests.RequestException:
        return JsonResponse({"error": "Error contacting user API"}, status=500)  # Internal Server Error

    try:
        user = User.objects.get(email=user_email)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)  # Not Found

    if not isinstance(user.events, list):
        return JsonResponse({"error": "Invalid data format for events"}, status=400)  # Bad Request

    try:
        event_ids = [event["id"] for event in user.events if isinstance(event, dict)]

        if id in event_ids:
            user.events = [event for event in user.events if event["id"] != id]
            user.save(update_fields=['events'])
            return JsonResponse({"message": "Event removed successfully"}, status=200)
        else:
            return JsonResponse({"error": "Event not found in saved event"}, status=404)  # Not Found

    except Exception as e:
        return JsonResponse({"error": f"Error removing event: {str(e)}"}, status=500)  

@login_required(login_url='/faculty/')
def toggle_event_status(request, id):
    if not request.user.is_staff or not request.user.is_active:
        messages.error(request, "Access denied. You must be an active faculty member to proceed.")
        
        storage = get_messages(request)
        print("Messages before redirect:", list(storage))  # Check if message exists

        return redirect(reverse('authentication:faculty'))
    
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=id)
            event.is_active = not event.is_active
            event.save()
            return JsonResponse({"message": "Event status updated successfully"}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({"error": "Event not found"}, status=404)  # Not Found
        except Exception as e:
            return JsonResponse({"error": f"Error updating Event status: {str(e)}"}, status=500)
    else:
        messages.error(request, "Invalid request method.")
        return redirect(reverse('authentication:faculty'))

@login_required(login_url='/faculty/')
def event_delete(request, id):
    event = Event.objects.filter(id=id).first()

    if not event:
        return JsonResponse({"success": False, "message": "Event not found"}, status=404)

    try:
        # Delete job from all users' saved events list
        users_with_events = User.objects.filter(events__contains=[{"id": id}])
        for user in users_with_events:
            user.events = [event for event in user.events if event.get("id") != id]
            user.save()

        # Delete the event itself
        event.delete()
        return JsonResponse({"success": True}, status=200)
    except Exception as e:
        return JsonResponse({"success": False, "message": "Internal server error"}, status=500)
