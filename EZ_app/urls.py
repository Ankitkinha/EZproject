from django.urls import path
from .views import user_login, upload_file, user_signup, email_verify, download_file, list_uploaded_files, user_logout

app_name = 'EZ_app'

urlpatterns = [
    path('login/', user_login, name='user-login'),
    path('upload-file/', upload_file, name='upload-file'),
    path('signup/', user_signup, name='user-signup'),
    path('email-verify/<str:uidb64>/<str:token>/', email_verify, name='email-verify'),
    path('download-file/<str:assignment_id>/', download_file, name='download-file'),
    path('list-uploaded-files/', list_uploaded_files, name='list-uploaded-files'),
    path('logout/', user_logout, name='user-logout'),
]
