from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        fields = '__all__'
        model = User


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.save()
        email_from = settings.EMAIL_HOST_USER
        user.email_user('Verification Code', 'Here is verification code',
                        email_from)
        return user
