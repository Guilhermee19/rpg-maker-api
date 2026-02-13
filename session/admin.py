from django.contrib import admin
from django import forms
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Session, SessionMember, SessionInvite, SessionCharacter


# Garantir que User tenha search_fields para autocomplete
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['username', 'email', 'first_name', 'last_name']


class SessionMemberInline(admin.TabularInline):
    model = SessionMember
    extra = 0
    readonly_fields = ['joined_at']
    autocomplete_fields = ['user']


class SessionCharacterInline(admin.TabularInline):
    model = SessionCharacter
    extra = 0
    readonly_fields = ['joined_at']
    autocomplete_fields = ['user', 'character']


class SessionInviteInline(admin.StackedInline):
    model = SessionInvite
    extra = 0
    readonly_fields = ['id', 'uses_count', 'created_at']
    fields = ['code', 'max_uses', 'uses_count', 'expires_at', 'created_at']


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'master', 'system_key', 'status', 
        'member_count', 'character_count', 'created_at'
    ]
    list_filter = ['status', 'system_key', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'master__username', 'master__email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    autocomplete_fields = ['master']
    list_editable = ['status']
    list_per_page = 25
    
    inlines = [SessionMemberInline, SessionCharacterInline, SessionInviteInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id', 'name', 'description', 'master', 'system_key')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    def member_count(self, obj):
        count = obj.members.count()
        url = reverse('admin:session_sessionmember_changelist') + f'?session__id__exact={obj.id}'
        return format_html('<a href="{}">{} membros</a>', url, count)
    member_count.short_description = 'Membros'
    
    def character_count(self, obj):
        count = obj.session_characters.count() 
        url = reverse('admin:session_sessioncharacter_changelist') + f'?session__id__exact={obj.id}'
        return format_html('<a href="{}">{} personagens</a>', url, count)
    character_count.short_description = 'Personagens'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('master').prefetch_related('members', 'session_characters')


@admin.register(SessionMember)
class SessionMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'role', 'joined_at']
    list_filter = ['role', 'joined_at', 'session__status', 'session__system_key']
    search_fields = ['user__username', 'user__email', 'session__name']
    readonly_fields = ['id', 'joined_at']
    autocomplete_fields = ['user', 'session']
    list_per_page = 50
    
    fieldsets = (
        ('Membro da Sessão', {
            'fields': ('id', 'session', 'user', 'role')
        }),
        ('Datas', {
            'fields': ('joined_at',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'session')


@admin.register(SessionInvite)
class SessionInviteAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'session', 'max_uses', 'uses_count', 
        'is_expired', 'is_unlimited', 'created_at'
    ]
    list_filter = ['created_at', 'max_uses', 'session__status']
    search_fields = ['code', 'session__name']
    readonly_fields = ['id', 'uses_count', 'created_at']
    autocomplete_fields = ['session']
    
    fieldsets = (
        ('Convite', {
            'fields': ('id', 'session', 'code')
        }),
        ('Limitações de Uso', {
            'fields': ('max_uses', 'uses_count', 'expires_at')
        }),
        ('Datas', {
            'fields': ('created_at',)
        }),
    )
    
    def is_expired(self, obj):
        if obj.expires_at:
            expired = timezone.now() > obj.expires_at
            return format_html(
                '<span style="color: {};">{}</span>',
                'red' if expired else 'green',
                'Expirado' if expired else 'Válido'
            )
        return 'Sem expiração'
    is_expired.short_description = 'Status'
    
    def is_unlimited(self, obj):
        if obj.max_uses is None:
            return format_html('<span style="color: green;">Ilimitado</span>')
        elif obj.uses_count >= obj.max_uses:
            return format_html('<span style="color: red;">Esgotado</span>')
        else:
            remaining = obj.max_uses - obj.uses_count
            return format_html('<span style="color: orange;">{} restantes</span>', remaining)
    is_unlimited.short_description = 'Usos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session')


@admin.register(SessionCharacter)
class SessionCharacterAdmin(admin.ModelAdmin):
    list_display = ['character_name', 'user', 'session', 'character_system', 'joined_at']
    list_filter = ['joined_at', 'session__status', 'character__system_key']
    search_fields = [
        'character__player_name', 'user__username', 'user__email', 
        'session__name'
    ]
    readonly_fields = ['id', 'joined_at']
    autocomplete_fields = ['user', 'session', 'character']
    
    fieldsets = (
        ('Personagem na Sessão', {
            'fields': ('id', 'session', 'user', 'character')
        }),
        ('Datas', {
            'fields': ('joined_at',)
        }),
    )
    
    def character_name(self, obj):
        if obj.character:
            url = reverse('admin:characters_character_change', args=[obj.character.id])
            return format_html('<a href="{}">{}</a>', url, obj.character.player_name or 'Sem nome')
        return 'N/A'
    character_name.short_description = 'Personagem'
    
    def character_system(self, obj):
        return obj.character.system_key if obj.character else 'N/A'
    character_system.short_description = 'Sistema'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'session', 'character')