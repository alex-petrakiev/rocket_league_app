from django.contrib import admin
from .models import Clip, Rating


@admin.register(Clip)
class ClipAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_approved', 'views_count', 'created_at')
    list_filter = ('is_approved', 'category', 'created_at')
    search_fields = ('title', 'author__username', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('views_count', 'created_at')
    actions = ['approve_clips', 'reject_clips']

    def approve_clips(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} clips approved successfully.')

    approve_clips.short_description = 'Approve selected clips'

    def reject_clips(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} clips rejected.')

    reject_clips.short_description = 'Reject selected clips'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'clip', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user__username', 'clip__title')
    ordering = ('-created_at',)