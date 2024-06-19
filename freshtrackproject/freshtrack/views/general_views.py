from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from freshtrack.tasks import check_expirations
from freshtrack.utility import get_notifications_for_user
from freshtrack.models import Notification
from freshtrack.tasks import check_expirations

def index(request):
    check_expirations()
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

@login_required
def notifications_view(request):
    # Esegui il controllo delle scadenze
    check_expirations()

    # Ottieni tutte le notifiche dell'utente
    notifications = Notification.objects.filter(user=request.user)

    # Conta le notifiche non lette
    unread_count = notifications.filter(is_read=False).count()

    # Passa le notifiche e il conteggio delle notifiche non lette al template
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'notifications_count': unread_count,
    })
