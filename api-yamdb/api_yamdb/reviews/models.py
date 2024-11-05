from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from users.models import User


MAX_LENGTH_NAME = 256
MAX_LENGTH_SLUG = 50


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['slug'], name='category_slug_unique_idx'),
        ]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Идентификатор',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        indexes = [
            models.Index(fields=['slug'], name='genre_slug_unique_idx'),
        ]

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанры'
    )
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название'
    )
    year = models.IntegerField(verbose_name='Год выпуска')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'

    def __str__(self):
        return self.name

    @property
    def rating(self):
        average_rating = self.reviews.aggregate(average_score=Avg('score'))[
            'average_score'
        ]
        return round(average_rating) if average_rating is not None else None


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE,)
    title = models.ForeignKey(Title, on_delete=models.CASCADE,)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['genre', 'title'],
                                    name='unique_genre_title')
        ]

    def __str__(self) -> str:
        return f'{self.genre}, {self.title}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return f'Отзыв на {self.title} от {self.author}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)
        default_related_name = 'comments'

    def __str__(self):
        return f'Комментарий к отзыву {self.review}'
