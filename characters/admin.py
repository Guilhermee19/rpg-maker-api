from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea
from django.utils.html import format_html
from .models import Character, RPGSystem


class RPGSystemAdminForm(forms.ModelForm):
    class Meta:
        model = RPGSystem
        fields = ['name', 'description', 'base_sheet_data', 'is_active', 'is_default']
        widgets = {
            'base_sheet_data': Textarea(attrs={'rows': 20, 'cols': 80, 'style': 'font-family: monospace;'}),
            'description': Textarea(attrs={'rows': 4, 'cols': 80}),
        }


@admin.register(RPGSystem)
class RPGSystemAdmin(admin.ModelAdmin):
    form = RPGSystemAdminForm
    list_display = ['name', 'slug', 'is_active', 'is_default', 'character_count', 'created_at']
    list_filter = ['is_active', 'is_default', 'created_at']
    search_fields = ['name', 'slug', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    list_editable = ['is_active', 'is_default']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description')
        }),
        ('Template da Ficha', {
            'fields': ('base_sheet_data',),
            'classes': ('collapse',)
        }),
        ('Configurações', {
            'fields': ('is_active', 'is_default')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def character_count(self, obj):
        """Conta quantos personagens usam este sistema"""
        count = obj.characters.count()
        if count > 0:
            return format_html('<span style="color: green;">{} personagens</span>', count)
        # Corrigido: format_html sem variáveis causava TypeError
        return format_html('<span style="color: gray;">Nenhum personagem</span>')
    character_count.short_description = 'Personagens'

    actions = ['duplicate_system']
    
    def duplicate_system(self, request, queryset):
        """Ação para duplicar sistemas selecionados"""
        count = queryset.count()
        for system in queryset:
            original_name = system.name
            system.pk = None
            system.slug = None  # força geração de novo slug pelo save()
            system.name = f"{original_name} (Cópia)"
            system.is_default = False
            system.save()
        self.message_user(request, f'{count} sistema(s) duplicado(s) com sucesso.')
    duplicate_system.short_description = 'Duplicar sistemas selecionados'


class CharacterAdminForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = '__all__'
        widgets = {
            'sheet_data': Textarea(attrs={'rows': 20, 'cols': 80, 'style': 'font-family: monospace;'}),
        }


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm
    list_display = ['player_name', 'user', 'rpg_system_name', 'xp_total', 'is_active', 'created_at']
    list_filter = ['rpg_system', 'is_active', 'created_at', 'updated_at']
    search_fields = ['player_name', 'user__username', 'user__email', 'rpg_system__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('user', 'player_name', 'rpg_system')
        }),
        ('Progressão', {
            'fields': ('xp_total', 'avatar_url', 'description')
        }),
        ('Dados da Ficha', {
            'fields': ('sheet_data',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'updated_at')
        }),
    )
    
    def rpg_system_name(self, obj):
        """Exibe o nome do sistema de RPG"""
        if obj.rpg_system:
            return obj.rpg_system.name
        # Corrigido: era obj.system_key que não existe no modelo
        return obj.system_name  # property definida no model: "Sistema não definido"
    rpg_system_name.short_description = 'Sistema RPG'
    rpg_system_name.admin_order_field = 'rpg_system__name'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'rpg_system')