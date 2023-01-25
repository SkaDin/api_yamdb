from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token

from reviews.models import Genre, Category, Title, Review, Comments

User = get_user_model()


class UserBaseSerializer(serializers.ModelSerializer):
    """User model base serializer."""
    username = serializers.CharField(
        max_length=settings.USERNAME_MAX_LENGTH, validators=[
            UnicodeUsernameValidator(), ])
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        if not User.objects.filter(**attrs).exists():
            self.validate_attribute({'username': attrs.get('username')})
            self.validate_attribute({'email': attrs.get('email')})
        return attrs

    def validate_attribute(self, attr):
        if User.objects.filter(
                **attr).exists():
            raise serializers.ValidationError(
                f'User with {attr} exists',
            )

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        return user


class UserSerializer(UserBaseSerializer):
    """User model serializer."""

    class Meta(UserBaseSerializer.Meta):
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role')


class RegisterSerializer(UserBaseSerializer):
    """Registration serializer"""

    class Meta(UserBaseSerializer.Meta):
        fields = ('username', 'email',)

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                'Username "me" is not allowed.')
        return username


class TokenObtainPairSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True, source='key')

    class Meta:
        fields = ('username', 'confirmation_code')
        model = Token

    def validate(self, attrs):
        user = get_object_or_404(User,
                                 username=attrs.get(
                                     'username'))
        if not (user.auth_token.key == attrs.get(
                'confirmation_code')):
            raise serializers.ValidationError(
                'Confirmation code is invalid.')
        return user


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
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
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = (
            'text',
            'score',
            'id',
            'author',
            'pub_date',
        )


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
