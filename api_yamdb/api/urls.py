from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet, \
    RegisterViewSet, TokenObtainPairView

v1_router = DefaultRouter()
v1_router.register(r'auth/signup', RegisterViewSet, basename='signup')
v1_router.register(r'auth/token', TokenObtainPairView, basename='signup')
v1_router.register(r'categories', CategoryViewSet, basename='categories')
v1_router.register(r'genres', GenreViewSet, basename='genres')
v1_router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
