from django.shortcuts import render, redirect
from django.contrib.auth import login,logout,authenticate
from .forms import UserRegistrationForm, UserLoginForm 
from .models import Event
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

#Api_code_import
from .serializers import EventSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response



def home(request):
    query = request.GET.get('q') 
    if query:
        events = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(location_name__icontains=query)
        )
    else:
        events = Event.objects.all()

    context = {'events': events, 'query': query}
    return render(request, 'eventapp/home.html', context)


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('eventapp:home')  
    else:
        form = UserRegistrationForm()

    return render(request, 'eventapp/user_registration.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('eventapp:home')


def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('eventapp:home') 
    else:
        form = UserLoginForm()

    return render(request, 'eventapp/login.html', {'form': form})
@login_required(login_url='eventapp:login')
def enroll_for_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    if user in event.registered_users.all():
        # User is already registered for the event
        messages.warning(request, 'You are already registered for this event.')
        return redirect('eventapp:home')

    if event.available_slots() > 0:
        event.registered_users.add(user)
        messages.success(request, 'Successfully enrolled for the event.')
        return redirect('eventapp:home')
    else:
        # Event is full
        messages.error(request, 'Sorry, the event is full. Unable to enroll.')
        return redirect('eventapp:home')
    
@login_required(login_url='eventapp:login')
def user_dashboard(request):
    user_registered_events = request.user.registered_events.all()
    total_registered_events = user_registered_events.count()

    return render(request, 'eventapp/user_dashboard.html', {
        'user_registered_events': user_registered_events,
        'total_registered_events': total_registered_events
    })
@login_required(login_url='eventapp:login')
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    if user in event.registered_users.all():
        event.registered_users.remove(user)
        messages.error(request, 'Successfully unenrolled for the event')
        return redirect('eventapp:user-dashboard')
    else:
        # User is not registered for the event
        return redirect('eventapp:user-dashboard')





# ------------------API Views-------------------

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetail(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_registered_events(request):
    user = request.user
    registered_events = user.registered_events.all()
    serializer = EventSerializer(registered_events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    user = request.user

    if user in event.registered_users.all():
        return Response({'message': 'User is already registered for the event.'}, status=status.HTTP_400_BAD_REQUEST)

    if event.available_slots() > 0:
        event.registered_users.add(user)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': 'Event is full. Unable to enroll.'}, status=status.HTTP_400_BAD_REQUEST)

