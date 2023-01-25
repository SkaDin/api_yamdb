from django.contrib import admin

from .models import Review, Comments, Title, Genre, Category

admin.site.register(Review)
admin.site.register(Comments)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Category)
