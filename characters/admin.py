from django.contrib import admin
from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'player_name', 'user', 'system_key', 'xp_total', 'is_active', 'created_at']
    list_filter = ['system_key', 'is_active', 'created_at', 'updated_at']
    search_fields = ['name', 'player_name', 'user__username', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'user', 'name', 'player_name', 'system_key')
        }),
        ('Progressão', {
            'fields': ('xp_total', 'portrait_url')
        }),
        ('Dados da Ficha', {
            'fields': ('sheet_data',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')