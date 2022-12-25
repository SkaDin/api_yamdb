from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, TokenObtainPairSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer
)
from api.permissions import (
    IsAuthenticatedOrReadOnly,
    UserPermissions,
    ModeratorPermissions,
    AdminPermissions,
)
from reviews.models import Category, Genre, Title, Review


User = get_user_model()


class CreateOnlyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RegisterViewSet(CreateOnlyViewSet):
    """View set of User model."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class TokenObtainPairView(CreateOnlyViewSet):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User,
                                 username=serializer.data.get('username'))
        if not (user.auth_token.key == serializer.data.get(
                'confirmation_code')):
            return Response('Confirmation code is invalid.',
                            status=status.HTTP_403_FORBIDDEN)
        token = RefreshToken.for_user(user)
        user.auth_token = None
        user.is_verified = True
        user.save()
        data = {
            'refresh': str(token),
            'access': str(token.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CategoryGenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass

class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    #filter_backends = (SearchFilter,)
    #search_fields = ('name')
    

class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    #filter_backends = (SearchFilter,)
    #search_fields = ('name')
    

class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
