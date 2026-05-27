from django.db import models
from django.contrib.auth import get_user_model
from core.models import IsPublished, CreatedAt


User = get_user_model()


class Category(IsPublished, CreatedAt):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=(
            'Идентификатор страницы для URL;'
            ' разрешены символы латиницы, цифры, дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class Location(IsPublished, CreatedAt):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(IsPublished, CreatedAt):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )

    image = models.ImageField(
        'Фото',
        upload_to='post_images',
        blank=True
    )

    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем —'
            ' можно делать отложенные публикации.'
        )
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog',
        verbose_name='Автор публикации',
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog',
        verbose_name='Местоположение',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='blog',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.post.count()


class Comment(CreatedAt):
    text = models.TextField('Текст комментария')

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='post',
        verbose_name='Пост'
    )

    author = models.ForeignKey(
        User,
        related_name='author',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
