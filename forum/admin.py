from django.contrib import admin
from .models import ForumPost, Comment


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_pinned', 'views_count', 'created_at')
    list_filter = ('category', 'is_pinned', 'created_at')
    search_fields = ('title', 'author__username', 'content')
    ordering = ('-created_at',)
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    actions = ['pin_posts', 'unpin_posts']

    def pin_posts(self, request, queryset):
        queryset.update(is_pinned=True)
        self.message_user(request, f'{queryset.count()} posts pinned successfully.')

    pin_posts.short_description = 'Pin selected posts'

    def unpin_posts(self, request, queryset):
        queryset.update(is_pinned=False)
        self.message_user(request, f'{queryset.count()} posts unpinned.')

    unpin_posts.short_description = 'Unpin selected posts'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'content_preview')
    list_filter = ('created_at',)
    search_fields = ('post__title', 'author__username', 'content')
    ordering = ('-created_at',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

    content_preview.short_description = 'Content Preview'