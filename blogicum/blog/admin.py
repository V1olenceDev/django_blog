from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Post, Category, Location


@register(Post)
class AdminPost(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'location',
        'category',
    )
    list_editable = (
        'is_published',
        'category',
        'location',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Category)
admin.site.register(Location)
