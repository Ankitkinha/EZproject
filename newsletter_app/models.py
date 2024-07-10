from django.db import models


class User(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=200)
    subscribe = models.BooleanField(default=False)
    created_id = models.DateTimeField(auto_now_add=True)


class UserChild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=200)
    age = models.IntegerField()


class JobScheduler(models.Model):
    job_name = models.CharField(max_length=200)
    schedule_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class Content(models.Model):
    age = models.IntegerField()
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


