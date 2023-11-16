from django.db import models


class PublishedModel(models.Model):
    """Абстрактная модель. Добавляет флаг is_published и created_at"""

    is_published = models.BooleanField(
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.',
        verbose_name='Опубликовано'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True,
        ordering = ('-created_at',)
