from django.contrib.auth import get_user_model
from django.db import models

from blog.constants import (LENGTH_OF_CATEGORY_TITLE, LENGTH_OF_COMMENT_TEXT,
                            LENGTH_OF_LOCATION_NAME, LENGTH_OF_POST_TITLE,
                            LENGTH_OF_STRING)
from core.models import PublishedModel

User = get_user_model()


class Category(PublishedModel):
    """Модель тематической категории,
    в которой собраны посты по определённой теме.
    """

    title = models.CharField(
        max_length=LENGTH_OF_STRING,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, '
                   'цифры, дефис и подчёркивание.'),
        verbose_name='Идентификатор'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)

    def __str__(self):
        return self.title[:LENGTH_OF_CATEGORY_TITLE]


class Location(PublishedModel):
    """Модель географической метки,
    одно определённое местоположение, к которому относится пост
    """

    name = models.CharField(
        max_length=LENGTH_OF_STRING,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:LENGTH_OF_LOCATION_NAME]


class Post(PublishedModel):
    """Модель отдельной публикации"""

    title = models.CharField(
        max_length=LENGTH_OF_STRING,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        help_text=('Если установить дату и время в будущем '
                   '— можно делать отложенные публикации.'),
        verbose_name='Дата и время публикации'
    )
    image = models.ImageField(
        upload_to='posts_images',
        blank=True,
        verbose_name='Фото'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='locations',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.title}'[:LENGTH_OF_POST_TITLE]


class Comment(models.Model):
    """Модель комментариев"""

    text = models.TextField(
        verbose_name='Комментарий'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Опубликован'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.text[:LENGTH_OF_COMMENT_TEXT]
