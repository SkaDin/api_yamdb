from django.db.models import Avg

from api.permissions import (AdminOrReadOnly, AdminOrSuperUserPermissions,
                             AdminPermissions, IsAdminOrIsSelf,
                             ReviewPermission, )
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, RegisterSerializer,
                             ReviewSerializer, TitleCreateSerializer,
                             TitleSerializer, TokenObtainPairSerializer,
                             UserSerializer,
                             )
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter

User = get_user_model()


class ListViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    pass


class CreateListDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class CreateViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
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
        return get_object_or_404(User, username=self.kwargs.get('pk'))

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAdminOrIsSelf, ])
    def me(self, request):
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
        response = super().create(request, args, kwargs)
        response.status_code = status.HTTP_200_OK
        return response

    def perform_create(self, serializer):
        user = serializer.save()
        email_from = settings.EMAIL_HOST_USER
        Token.objects.filter(user=user).delete()
        confirmation_code = Token.objects.create(user=user)
        user.email_user('Verification Code',
                        f'Here is confirmation code: {confirmation_code}',
                        email_from)


class TokenObtainPairView(CreateViewSet):
    """View set of token obtain."""
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


class CategoryViewSet(CreateListDestroyViewSet):
    """View set of categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(CreateListDestroyViewSet):
    """View set of genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(ModelViewSet):
    """View set of titles."""
    queryset = Title.objects.order_by('-id').all().annotate(
        rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TitleFilter

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (AllowAny(),)
        return (AdminPermissions(),)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewsViewSet(viewsets.ModelViewSet):
    """View set of reviews."""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        return get_object_or_404(
            Title, id=self.kwargs.get('title_id')
        ).reviews.all()

    def create(self, request, *args, **kwargs):
        reviews = self.get_queryset()
        if reviews.filter(author=self.request.user).exists():
            return Response("Error", status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, args, kwargs)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title_id=self.kwargs.get('title_id')

        )


class CommentsViewSet(viewsets.ModelViewSet):
    """View set of comments."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        ).comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review,
                                   id=self.kwargs.get('review_id'))
        return serializer.save(
            author=self.request.user,
            review=review
        )
