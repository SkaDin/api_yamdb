from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    RegisterViewSet,
    TokenObtainPairView,
    UserViewSet,
    ReviewsViewSet,
    CommentsViewSet
)

v1_router = DefaultRouter()

v1_router.register(r'auth/signup', RegisterViewSet, basename='signup')
v1_router.register(r'auth/token', TokenObtainPairView, basename='signup')
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'users/(?P<username>.+)/', UserViewSet,
                   basename='users')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet, basename='comments'
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
