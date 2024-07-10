from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, JobScheduler
from .task import send_newsletter
from django.views.decorators.http import require_POST


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        user, created = User.objects.get_or_create(email=email, defaults={'name': name})
        if not created:
            user.name = name
        user.subscribe = True
        user.save()
        return redirect('payment')  # Redirect to payment page
    return render(request, 'subscribe.html')


@require_POST
def schedule_newsletter(request):
    job_name = request.POST.get('job_name')
    job = JobScheduler.objects.create(job_name=job_name)
    send_newsletter.apply_async()  # Schedule the task immediately for simplicity
    return HttpResponse('Newsletter scheduled successfully.')


def payment(request):
    # payment processing logic here
    return render(request, 'payment.html')
