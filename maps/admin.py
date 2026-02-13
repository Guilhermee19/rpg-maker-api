from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import SessionMap


@admin.register(SessionMap)
class SessionMapAdmin(admin.ModelAdmin):
    list_display = ['name', 'session_link', 'grid_enabled', 'dimensions', 'status_icon', 'created_at']
    list_filter = ['is_active', 'grid_enabled', 'created_at', 'session']
    search_fields = ['name', 'session__name', 'session__master__username']
    readonly_fields = ['id', 'created_at', 'preview_image']
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'session', 'is_active')
        }),
        ('Configurações do Mapa', {
            'fields': ('image_url', 'preview_image', 'width', 'height')
        }),
        ('Configurações da Grade', {
            'fields': ('grid_enabled', 'grid_size')
        }),
        ('Metadados', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        })
    )
    
    # Configurações de exibição
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    # Ações em massa
    actions = ['activate_maps', 'deactivate_maps', 'enable_grid', 'disable_grid']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session', 'session__master')
    
    def session_link(self, obj):
        """Link para a sessão do mapa"""
        if obj.session:
            url = reverse('admin:session_session_change', args=[obj.session.pk])
            return format_html('<a href="{}">{}</a>', url, obj.session.name)
        return '-'
    session_link.short_description = 'Sessão'
    session_link.admin_order_field = 'session__name'
    
    def dimensions(self, obj):
        """Exibe as dimensões do mapa"""
        if obj.width and obj.height:
            return f"{obj.width} x {obj.height}"
        return 'Não definido'
    dimensions.short_description = 'Dimensões'
    
    def status_icon(self, obj):
        """Ícone de status do mapa"""
        if obj.is_active:
            return format_html('<span style="color: green;">●</span> Ativo')
        else:
            return format_html('<span style="color: red;">●</span> Inativo')
    status_icon.short_description = 'Status'
    status_icon.admin_order_field = 'is_active'
    
    def preview_image(self, obj):
        """Preview da imagem do mapa"""
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-width: 200px; max-height: 150px;" />',
                obj.image_url
            )
        return 'Sem imagem'
    preview_image.short_description = 'Preview'
    
    # Ações em massa
    def activate_maps(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} mapa(s) ativado(s) com sucesso.')
    activate_maps.short_description = 'Ativar mapas selecionados'
    
    def deactivate_maps(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} mapa(s) desativado(s) com sucesso.')
    deactivate_maps.short_description = 'Desativar mapas selecionados'
    
    def enable_grid(self, request, queryset):
        updated = queryset.update(grid_enabled=True)
        self.message_user(request, f'Grade ativada para {updated} mapa(s).')
    enable_grid.short_description = 'Ativar grade nos mapas selecionados'
    
    def disable_grid(self, request, queryset):
        updated = queryset.update(grid_enabled=False)
        self.message_user(request, f'Grade desativada para {updated} mapa(s).')
    disable_grid.short_description = 'Desativar grade nos mapas selecionados'
    