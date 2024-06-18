from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from freshtrack.tasks import check_expirations
from freshtrack.utility import get_notifications_for_user

def index(request):
    check_expirations()
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def notifications_view(request):
    notifications = get_notifications_for_user(request.user)
    return render(request, 'notifications.html', {
        'notifications': notifications,
    })