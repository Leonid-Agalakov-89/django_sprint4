from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import ModelFormMixin

from blog.constants import PAGINATOR
from blog.forms import CommentForm
from blog.mixins import CommentMixin, DispatchMixin, PostMixin
from blog.models import Category, Post, User
from blog.utils import filtered_select_posts


class PostListView(ListView):
    """CBV-класс для представления публикаций на главной странице"""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = PAGINATOR
    queryset = filtered_select_posts(
        Post
        .objects
        .prefetch_related('comments')
    )


class PostDetailView(DetailView):
    """CBV-класс для представления страницы отдельной публикации"""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
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
                pk=self.kwargs.get(self.pk_url_kwarg)))
        return (get_object_or_404(
            filtered_select_posts(self.model.objects),
                pk=self.kwargs.get(self.pk_url_kwarg)))


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """CBV-класс для создания новой публикации"""

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(LoginRequiredMixin, PostMixin, DispatchMixin, UpdateView):
    """CBV-класс для редактирования публикации"""

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']}
        )


class PostDeleteView(LoginRequiredMixin, PostMixin, DispatchMixin,
                     ModelFormMixin, DeleteView):
    """CBV-класс для удаления публикации"""

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """CBV-класс для создания нового комментария к публикации"""

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, CommentMixin,
                        DispatchMixin, UpdateView):
    """CBV-класс для редактирования комментария к публикации"""


class CommentDeleteView(LoginRequiredMixin, CommentMixin,
                        DispatchMixin, DeleteView):
    """CBV-класс для удаления комментария к публикации"""


class ProfileListView(ListView):
    """CBV-класс для представления страницы пользователя"""

    model = Post
    template_name = 'blog/profile.html'
    paginate_by = PAGINATOR

    def get_queryset(self):
        profile = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return profile.users.all().annotate(
            comment_count=Count('comments')).order_by('-pub_date',)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return context


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
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class CategoryListView(ListView):
    """CBV-класс для представления страницы категории"""

    model = Post
    template_name = 'blog/category.html'
    paginate_by = PAGINATOR
    slug_url_kwarg = 'category_slug'

    def get_queryset(self):
        category = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug'), is_published=True)
        return filtered_select_posts(category.posts.all())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, slug=self.kwargs.get('category_slug'))
        return context
