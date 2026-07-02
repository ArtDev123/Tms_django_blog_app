from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'author')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    date_hierarchy = 'created_at'
