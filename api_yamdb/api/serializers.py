from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from reviews.models import Genre, Category, Title


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
        # TODO Create method to send emails with verification code.
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.save()
        return user


class GenreSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class TitleSerializer(ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title