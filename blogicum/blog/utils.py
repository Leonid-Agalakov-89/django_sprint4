from django.db.models import Count
from django.utils import timezone


def filtered_select_posts(posts):
    """
    Функция с кодом, который повторяется в представлениях blog.views:
    pub_date__lte=timezone.now() - Дата публикации — не позже текущего времени;
    is_published=True - Пост разрешён к публикации;
    category__is_published=True - Категория разрешена к публикации;
    comment_count=Count('comments') - Подсчёт количества комментариев;
    order_by('-pub_date') - Сортировка публикаций по дате.
    """
    return posts.select_related(
        'location', 'category', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
