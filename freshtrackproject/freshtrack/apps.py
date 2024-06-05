from django.apps import AppConfig
from django_q.tasks import schedule
from django_q.models import Schedule


class FreshtrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freshtrack'

    Schedule.objects.filter(name='check_expirations').delete()

    # Pianifica il task per eseguirsi ogni giorno
    schedule(
        'myapp.tasks.check_expirations',
        name='check_expirations',
        schedule_type=Schedule.HOURLY
    )
