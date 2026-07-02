from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'author')
    search_fields = ('text', 'post__title')
    list_editable = ('is_active',)

