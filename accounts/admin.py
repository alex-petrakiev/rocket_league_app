from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_rank')
    list_filter = UserAdmin.list_filter + ('userprofile__current_rank',)

    def get_rank(self, obj):
        return obj.userprofile.current_rank.title() if hasattr(obj, 'userprofile') else 'No Profile'

    get_rank.short_description = 'Rank'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_rank', 'hours_played', 'location', 'created_at')
    list_filter = ('current_rank', 'created_at')
    search_fields = ('user__username', 'user__email', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)