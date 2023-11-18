from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Category, Comment, Location, Post

admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


class CommentAdmin(admin.ModelAdmin):
    empty_value_display = 'Не задано'


class PostAdmin(admin.ModelAdmin):
    inlines = (
        CommentInline,
    )
    list_display = (
        '__str__',
        'title',
        'text',
        'pub_date',
        'is_published',
        'author',
        'location',
        'category',
    )
    list_editable = (
        'is_published',
        'author',
        'location',
        'category'
    )
    search_fields = ('title',)
    list_filter = ('is_published',
                   'author',
                   'location',
                   'category'
                   )
    list_display_links = ('title',)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
