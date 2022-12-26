from .permissions import AdminPermissions
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, TokenObtainPairSerializer, \
    UserSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from .filters import TitleFilter
from rest_framework.pagination import PageNumberPagination
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
    ReviewSerializer,
    TitleCreateSerializer
)
from api.permissions import (
    IsAuthenticatedOrReadOnly,
    UserPermissions,
    ModeratorPermissions,
    AdminPermissions,
    IsAdminUser,
    AdminOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from reviews.models import Category, Genre, Title, Reviews
from django.db.models import Avg


User = get_user_model()


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class ListViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    pass


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermissions,)  # Todo Set Permission to IsAuthenticated
    pagination_class = PageNumberPagination


class RegisterViewSet(CreateViewSet):
    """View set of users registration."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


class TokenObtainPairView(CreateViewSet):
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
                            status=status.HTTP_400_BAD_REQUEST)
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
    #search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (AdminPermissions(),)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions)

    def get_queryset(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        ).reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
        )
