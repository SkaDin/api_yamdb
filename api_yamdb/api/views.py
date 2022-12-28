from api.permissions import (AdminOrReadOnly, AdminOrSuperUserPermissions,
                             AdminPermissions, IsAdminOrIsSelf,
                             IsAdminUser,
                             IsAuthenticatedOrReadOnly,
                             ModeratorPermissions,
                             UserPermissions)
from api.serializers import (CategorySerializer, GenreSerializer,
                             RegisterSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleSerializer,
                             TokenObtainPairSerializer, UserSerializer)
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter

User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class ListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class UserViewSet(ModelViewSet):
    """View set of users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('username',)
    permission_classes = [AdminOrSuperUserPermissions, ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_object(self):
        username = self.kwargs.get('pk')
        return get_object_or_404(User, username=username)

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAdminOrIsSelf, ])
    def me(self, request, ):
        instance = request.user
        if self.request.method == 'GET':
            serializer = self.get_serializer(instance)
        else:
            serializer = self.get_serializer(instance, data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=instance.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterViewSet(CreateViewSet):
    """View set of users registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        return get_object_or_404(User, **self.kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = serializer.save()
        email_from = settings.EMAIL_HOST_USER
        Token.objects.filter(user=user).delete()
        confirmation_code = Token.objects.create(user=user)
        user.email_user('Verification Code',
                        f'Here is confirmation code: {confirmation_code}',
                        email_from)


class TokenObtainPairView(CreateViewSet):
    serializer_class = TokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = self.create_token(request.user)
        return Response(token, status=status.HTTP_201_CREATED)

    @staticmethod
    def create_token(user):
        token = RefreshToken.for_user(user)
        Token.objects.filter(user=user).delete()
        user.is_verified = True
        user.save()
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }


class CategoryGenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all().order_by('-id')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all().order_by('-id')
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().order_by('-id')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    # search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return AllowAny(),
        return AdminPermissions(),

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )
