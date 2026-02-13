from django.contrib import admin
from django import forms
from django.forms.widgets import Textarea
from .models import Character


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
    list_display = ['player_name', 'user', 'system_key', 'xp_total', 'is_active', 'created_at']
    list_filter = ['system_key', 'is_active', 'created_at', 'updated_at']
    search_fields = ['player_name', 'user__username', 'user__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    list_editable = ['is_active']
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'user', 'player_name', 'system_key')
        }),
        ('Progressão', {
            'fields': ('xp_total', 'avatar_url')
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