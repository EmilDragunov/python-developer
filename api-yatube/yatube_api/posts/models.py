from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name=("Название"),
    )
    slug = models.SlugField(
        unique=True,
        verbose_name=("Слаг"),
        db_index=True,
    )
    description = models.TextField(
        verbose_name=("Описание"),
    )

    class Meta:
        ordering = ['title']
        verbose_name = ("Группа")
        verbose_name_plural = ("Группы")

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('Автор'),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=('Группа'),
    )
    text = models.TextField(
        verbose_name=('Текст'),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )
    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name=('Изображение'),
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = ("Пост")
        verbose_name_plural = ("Посты")
        default_related_name = 'posts'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('Автор'),
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name=('Пост'),
    )
    text = models.TextField(
        verbose_name=('Текст'),
    )
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['-created']
        verbose_name = ("Комментарий")
        verbose_name_plural = ("Комментарии")
        default_related_name = 'comments'

    def __str__(self):
        return f'{self.author} - {self.text[:15]}...'


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        default=None
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        default=None
    )

    class Meta:
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_name_follower'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
