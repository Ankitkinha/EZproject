from django.contrib import admin
from .models import User, UserChild, JobScheduler, Content

admin.site.register(User)
admin.site.register(UserChild)
admin.site.register(JobScheduler)
admin.site.register(Content)
