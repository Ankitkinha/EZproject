from rest_framework import serializers
from .models import User, UploadedFile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type', 'is_verified')
        read_only_fields = ('id', 'is_verified')


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'user', 'file', 'uploaded_at')
        read_only_fields = ('id', 'user', 'uploaded_at')
