from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'rarity', 'durability_current', 'durability_max')
    list_filter = ('category', 'rarity', 'session')
    search_fields = ('name', 'category', 'rarity', 'session__name')
    # raw_id_fields = ('session',)

    def session_link(self, obj):
        if obj.session:
            return f'<a href="/admin/session/session/{obj.session.id}/change/">{obj.session.name}</a>'
        return "-"
    session_link.allow_tags = True
    session_link.short_description = 'Session'