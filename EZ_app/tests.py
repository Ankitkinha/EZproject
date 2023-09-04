from django.test import TestCase
from EZ_app.models import User, UploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class UserLoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login_valid_credentials(self):
        user_data = {'username': 'testuser', 'password': 'testpassword'}

        response = self.client.post(reverse('EZ_app:user-login'), user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Login successful.')

    def test_user_login_invalid_credentials(self):
        invalid_user_data = {'username': 'invaliduser', 'password': 'invalidpassword'}

        response = self.client.post(reverse('EZ_app:user-login'), invalid_user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials.')


class UploadFileTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.operation_user = User.objects.create_user(username='operationuser', password='testpassword',
                                                       user_type='operation')
        self.client_user = User.objects.create_user(username='clientuser', password='testpassword', user_type='client')
        self.valid_file = open('path/to/valid/file.pptx', 'rb')  # Replace with a path to a valid file
        self.invalid_file = open('path/to/invalid/file.txt', 'rb')  # Replace with a path to an invalid file

    def test_upload_file_success(self):
        # Authenticate as an operation user
        self.client.force_authenticate(user=self.operation_user)

        response = self.client.post(reverse('EZ_app:upload-file'), {'file': self.valid_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_upload_file_invalid_format(self):
        # Authenticate as an operation user
        self.client.force_authenticate(user=self.operation_user)

        response = self.client.post(reverse('EZ_app:upload-file'), {'file': self.invalid_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UploadedFile.objects.count(), 0)  # No file should be uploaded

    def test_upload_file_unauthorized(self):
        # Authenticate as a client user
        self.client.force_authenticate(user=self.client_user)

        response = self.client.post(reverse('EZ_app:upload-file'), {'file': self.valid_file}, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # No file should be uploaded
        self.assertEqual(UploadedFile.objects.count(), 0)
