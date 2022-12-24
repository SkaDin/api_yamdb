from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from reviews.models import Category, Genre, Title
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
)
from api.permissions import (
    IsAuthenticatedOrReadOnly,
    UserPermissions,
    ModeratorPermissions,
    AdminPermissions,
)

User = get_user_model()


class CreateOnlyViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass

class CategoryGenreViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass

class RegisterViewSet(CreateOnlyViewSet):
    """View set of User model."""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)


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
