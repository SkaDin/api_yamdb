import inflect
from django.db import models
from users.models import User

from .validators import validator_year


class CategoryGenreBase(models.Model):
    name = models.CharField('Наименование', max_length=256)
    slug = models.SlugField(
        'Слаг',
        max_length=50,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Category(CategoryGenreBase):
    class Meta:
        verbose_name = 'Category'


class Genre(CategoryGenreBase):
    class Meta:
        verbose_name = 'Genre'


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
        verbose_name='Genre'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.CharField(
        max_length=400, verbose_name='Текст комментария:',
        help_text='Опишите свои впечатления:'
    )
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации:', auto_now_add=True
    )
    score = models.IntegerField(
        choices=[
            (
                x, inflect.engine().number_to_words(x)
            ) for x in range(1, 11)],
        blank=False,
        null=False,
    )
    title = models.ForeignKey(
        Title, related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведения:'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='Review from this author already exist.',
            )
        ]


class Comments(models.Model):
    text = models.CharField(verbose_name='Текст отзыва:', max_length=400)
    author = models.ForeignKey(
        User,
        related_name='comments',
        verbose_name='Автор отзыва:',
        on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(
        'Дата публикации:',
        auto_now_add=True,
    )
    review = models.ForeignKey(
        Review,
        related_name='comments',
        on_delete=models.CASCADE,
    )