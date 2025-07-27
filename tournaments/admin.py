from django.contrib import admin
from .models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'organizer', 'status', 'participants_count', 'max_participants', 'start_date')
    list_filter = ('status', 'start_date', 'created_at')
    search_fields = ('name', 'organizer__username', 'description')
    ordering = ('-start_date',)
    readonly_fields = ('participants_count', 'created_at')
    filter_horizontal = ('participants',)

    def participants_count(self, obj):
        return obj.participants.count()

    participants_count.short_description = 'Participants'