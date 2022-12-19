from django.db import models



class Category(models.Model):
    name = models.CharField('Наименование катерогии', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
    )

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField('Наименование жанра', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=56,
        unique=True
    )

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField('Наименование произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    genre = models.ManyToManyField(
        Genre,
        on_delete = models.CASCADE,
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
