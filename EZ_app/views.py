from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import UploadedFile, User
from django.contrib.auth import authenticate, login, logout
from django.core.signing import Signer
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer, UploadedFileSerializer


@action(detail=False, methods=['POST'])
def user_login(request):
    # Get username and password from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate user
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Login the user
        login(request, user)
        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@action(detail=False, methods=['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    # Check if the user is authenticated and is an operation user
    if request.user.user_type == 'operation':
        file = request.FILES.get('file')
        if file:
            file_type = file.name.split('.')[-1]
            if file_type in ['pptx', 'docx', 'xlsx']:
                uploaded_file = UploadedFile(user=request.user, file=file)
                uploaded_file.save()
                return Response({'message': 'File uploaded successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid file format.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'You are not authorized to perform this action.'}, status=status.HTTP_403_FORBIDDEN)


@action(detail=False, methods=['POST'])
def user_signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate a token for email verification
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build the verification URL
            current_site = get_current_site(request)
            verify_url = reverse('email-verify', kwargs={'uidb64': uid, 'token': token})
            verify_url = f'http://{current_site.domain}{verify_url}'

            # Send an email with the verification link
            subject = 'Verify your email'
            message = f'Click the following link to verify your email: {verify_url}'
            from_email = 'ankitkinha786@email.com'
            send_mail(subject, message, from_email, [user.email], fail_silently=False)

            return Response({'message': 'Please check your email for verification instructions.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@action(detail=False, methods=['GET'])
def email_verify(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), 'utf-8')
        user = User.objects.get(pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            return Response({'message': 'Email verification successful.'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Custom Signer for generating secure download URLs
signer = Signer()


@action(detail=False, methods=['GET'])
@permission_classes([IsAuthenticated])
def download_file(request, assignment_id):
    try:
        # Check if the user is a client user
        if request.user.user_type == 'client':
            # Generate a secure encrypted download URL
            encrypted_url = signer.sign(f'download-{assignment_id}')
            return Response({'download-link': encrypted_url, 'message': 'success'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You are not authorized to access this resource.'},
                            status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@action(detail=False, methods=['GET'])
@permission_classes([IsAuthenticated])
def list_uploaded_files(request):
    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user)
    serializer = UploadedFileSerializer(uploaded_files, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@action(detail=False, methods=['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
