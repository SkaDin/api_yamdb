from django.db import models
from .validators import validator_year

class CategoryGenreBase(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True
    )
    def __str__(self):
        return self.name
    class Meta:
        abstract = True



class Category(CategoryGenreBase):
    class Meta:
        verbose_name = 'Категория'


class Genre(CategoryGenreBase):
    class Meta:
        verbose_name = 'Жанр'


class Title(models.Model):
    name = models.CharField('Наименование произведения', max_length=256)
    year = models.IntegerField(
        'Год выпуска',
        validators=[validator_year],
    )
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория'
    )

    def __str__(self):
        return self.name
