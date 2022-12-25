from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token
import re

from reviews.models import Genre, Category, Title, Review

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
        fields = ('username', 'email',)
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=['username', 'email'],
                message='Already exists.'
            )
        ]

    def validate_username(self, username):
        pattern = re.compile('^[\w.@+-]+\Z')
        if not re.match(pattern, username):
            raise serializers.ValidationError('Username format is invalid')
        return username


class TokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True, source='key')

    class Meta:
        fields = ('username', 'confirmation_code')
        model = Token


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
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category'
        )


class ReviewSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score'
            'pub_date',
        )
