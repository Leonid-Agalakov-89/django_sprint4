from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post

admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


class LocationAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'title',
        'text',
        'pub_date',
        'is_published',
        'author',
        'location',
        'category'
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
