from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'session', 'category', 'rarity', 'durability_current', 'durability_max')
    list_filter = ('category', 'rarity', 'session')
    search_fields = ('name', 'category', 'rarity', 'session__name')
    raw_id_fields = ('session',)