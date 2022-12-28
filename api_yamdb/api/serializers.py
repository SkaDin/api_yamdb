from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
import re

from reviews.models import Genre, Category, Title, Reviews, Comments


User = get_user_model()


class UsernameValidator:
    requires_context = True
    format_message = 'Username format is invalid.'
    length_message = 'Username is too long.'
    LENGTH = 150

    def __init__(self, queryset, fields):
        self.queryset = queryset

    def __call__(self, attrs, serializer):
        pattern = re.compile('(?=(^(?!me$)))(?=(^[\w.@+-]+\Z))')
        username = attrs.get('username')
        if self.queryset.filter(username=username).exists():
            raise serializers.ValidationError(
                "Username %s already exists" % username)
        if not re.match(pattern, username):
            raise serializers.ValidationError(self.format_message)
        if len(username) > self.LENGTH:
            raise serializers.ValidationError(self.length_message)


class EmailValidator:
    requires_context = True
    message = 'Email format is invalid'
    LENGTH = 254

    def __init__(self, queryset, fields, ):
        self.queryset = queryset

    def __call__(self, attrs, serializer):
        email = attrs.get('email')
        # if self.queryset.filter(email=email).exists():
        #     raise serializers.ValidationError("Email is not unique")
        if len(attrs.get('email')) > self.LENGTH:
            raise serializers.ValidationError(self.message)


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')
        model = User


class RegisterSerializer(serializers.ModelSerializer):
    """Registration serializer"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [
            UsernameValidator(
                queryset=model.objects.all(),
                fields=['username', ],
            ),
            EmailValidator(
                queryset=model.objects.all(),
                fields=['email', ]
            )
        ]

    def create(self, validated_data):
        instance, _ = User.objects.get_or_create(
            **validated_data)
        return instance


class TokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True, source='key')

    class Meta:
        fields = ('username', 'confirmation_code')
        model = Token


class GenreSerializer(ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class ReviewSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Reviews
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        extra_kwargs = {
            'title': {'write_only': True}
        }

    # def validate(self, data):
    #     request = self.context['request']
    #     author = request.user
    #     title_id = self.context['view'].kwargs.get('title_id')
    #     if author.reviews.filter(title_id=title_id).exists():
    #         raise serializers.ValidationError('Oshibka')
    #     return data


class CommentSerializer(ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comments
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        extra_kwargs = {
            'review': {'write_only': True}
        }
