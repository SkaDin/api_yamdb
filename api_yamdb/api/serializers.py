from rest_framework.serializers import ModelSerializer
from reviews.models import Genre, Category, Title


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
        fields = '__all__'
        model = Title