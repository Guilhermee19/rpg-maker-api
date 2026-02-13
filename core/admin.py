from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_delete', 'created_at']
    list_filter = ['is_delete', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('Usuário', {
            'fields': ('user',)
        }),
        ('Perfil', {
            'fields': ('profile_image', 'is_delete')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )