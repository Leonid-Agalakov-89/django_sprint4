from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.constants import PAGINATOR
from blog.forms import CommentForm
from blog.mixins import CommentMixin, PostMixin
from blog.models import Category, Comment, Post, User


class PostListView(LoginRequiredMixin, ListView):
    """CBV-класс для представления публикаций на главной странице"""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGINATOR
    ordering = '-pub_date'
    queryset = (
        Post
        .objects
        .prefetch_related('comment')
        .select_related('author')
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True
        )
        .annotate(comment_count=Count('comment'))
    )


class PostDetailView(LoginRequiredMixin, DetailView):
    """CBV-класс для представления страницы отдельной публикации"""

    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = (self.object.comment.select_related('author'))
        return context

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        if post.author == self.request.user:
            return (get_object_or_404(
                self.model.objects
                .select_related(
                    'location',
                    'author',
                    'category'
                ),
                pk=self.kwargs.get('pk')))
        return (get_object_or_404(
            self.model.objects
                .select_related(
                    'location',
                    'author',
                    'category'
                ).filter(
                    pub_date__lte=timezone.now(),
                    is_published=True,
                    category__is_published=True
                ),
                pk=self.kwargs.get('pk')))


class PostCreateView(PostMixin, LoginRequiredMixin, CreateView):
    """CBV-класс для создания новой публикации"""

    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        self.request.user = self.get_object().username
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )


class PostUpdateView(PostMixin, LoginRequiredMixin, UpdateView):
    """CBV-класс для редактирования публикации"""

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:post_detail', pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'blog:post_detail', kwargs={'pk': self.kwargs['post_id']}
        )


class PostDeleteView(PostMixin, LoginRequiredMixin, DeleteView):
    """CBV-класс для удаления публикации"""

    success_url = reverse_lazy('blog:index')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            return redirect('blog:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDeleteView, self).get_context_data()
        context['form'] = self.form_class(instance=self.object)
        return context


class CommentCreateView(CommentMixin, LoginRequiredMixin, CreateView):
    """CBV-класс для создания нового комментария к публикации"""

    post_object = None

    def dispatch(self, request, *args, **kwargs):
        self.post_object = get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.post_object
        return super().form_valid(form)


class CommentUpdateView(CommentMixin, LoginRequiredMixin, UpdateView):
    """CBV-класс для редактирования комментария к публикации"""

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(CommentMixin, LoginRequiredMixin, DeleteView):
    """CBV-класс для удаления комментария к публикации"""

    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['comment_id'])
        if comment.author != request.user:
            return redirect('blog:post_detail', pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)


def profile(request, username):
    """View-функция для представления страницы профиля пользователя"""
    profile = get_object_or_404(User.objects.all(), username=username)
    user_posts = profile.users.all().annotate(
        comment_count=Count('comment')).order_by('-pub_date',)
    paginator = Paginator(user_posts, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': profile,
        'page_obj': page_obj
    }
    return render(request, 'blog/profile.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """CBV-класс для редактирования профиля пользователя"""

    model = User
    template_name = 'blog/user.html'
    fields = (
        'first_name',
        'last_name',
        'username',
        'email'
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        self.request.user = self.get_object().username
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user}
        )


def filtered_select_posts(posts):
    """
    Функция с кодом, который повторяется ниже:
    pub_date__lte=timezone.now() - Дата публикации — не позже текущего времени,
    is_published=True - Пост разрешён к публикации;
    category__is_published=True - Категория разрешена к публикации.
    """
    return posts.select_related(
        'location', 'category', 'author'
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def category_posts(request, category_slug):
    """View-функция для представления категории публикации"""
    category = get_object_or_404(
        Category.objects,
        is_published=True,
        slug=category_slug
    )
    post_list = filtered_select_posts(category.posts).annotate(
        comment_count=Count('comment')).order_by('-pub_date',)
    paginator = Paginator(post_list, PAGINATOR)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {
        'category': category, 'post_list': post_list, 'page_obj': page_obj})


def csrf_failure(request, reason=''):
    """
    View-функция для представления
    кастомной страницы ошибки 404 "Ошибка проверки CSRF, запрос отклонён"
    """
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    """
    View-функция для представления
    кастомной страницы ошибки 404 "Страница не найдена"
    """
    return render(request, 'pages/404.html', status=404)


def server_error(request, *args, **argv):
    """
    View-функция для представления
    кастомной страницы ошибки 500 "Сервер не может обработать запрос к сайту"
    """
    return render(request, 'pages/500.html', status=500)
