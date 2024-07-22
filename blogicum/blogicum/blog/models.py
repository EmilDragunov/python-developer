from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count


User = get_user_model()
TITLE = 'Заголовок'
NAME = 'Название места'
MAX_256 = 256
MAX_LENGTH = 10


class FilterManager(models.Manager):
    def published_posts(self):
        return super().filter(
            is_published=True,
            category__is_published=True,
            pub_date__lt=timezone.now()
        ).select_related(
            'author',
            'category',
            'location'
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')


class BaseModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Category(BaseModel):
    title = models.CharField(max_length=MAX_256, verbose_name=TITLE)
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
                  ' цифры, дефис и подчёркивание.'
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        indexes = [
            models.Index(fields=['slug']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return self.title[:MAX_LENGTH]


class Location(BaseModel):
    name = models.CharField(max_length=MAX_256, verbose_name=NAME)

    class Meta(BaseModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ['-created_at']

    def __str__(self):
        return self.name[:MAX_LENGTH]


class Post(BaseModel):
    title = models.CharField(max_length=MAX_256, verbose_name=TITLE)
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)
    objects = FilterManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
        default_related_name = 'posts'

    def __str__(self):
        return self.title[:MAX_LENGTH]


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:MAX_LENGTH]
