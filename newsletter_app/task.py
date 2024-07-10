from celery import shared_task
from django.core.mail import send_mail
from .models import User


@shared_task
def send_newsletter():
    subscribers = User.objects.filter(subscribe=True)
    for subscriber in subscribers:
        send_mail(
            'Your Newsletter',
            'Here will be the body of the newsletter.',
            'from@example.com',
            [subscriber.email],
            fail_silently=False,
        )
