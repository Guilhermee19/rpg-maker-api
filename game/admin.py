from django.contrib import admin
from .models import CharacterClass, Character, Item, CharacterItem, Skill, CharacterSkill


@admin.register(CharacterClass)
class CharacterClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_health', 'base_mana', 'base_attack', 'base_defense']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'character_class', 'level', 'owner', 'current_health', 'current_mana']
    list_filter = ['character_class', 'level', 'created_at']
    search_fields = ['name', 'owner__username']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'item_type', 'rarity', 'value']
    list_filter = ['item_type', 'rarity', 'created_at']
    search_fields = ['name', 'description']


@admin.register(CharacterItem)
class CharacterItemAdmin(admin.ModelAdmin):
    list_display = ['character', 'item', 'quantity', 'is_equipped']
    list_filter = ['is_equipped', 'item__item_type', 'created_at']
    search_fields = ['character__name', 'item__name']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'mana_cost', 'damage', 'healing', 'required_level']
    list_filter = ['required_level', 'mana_cost', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['character_classes']


@admin.register(CharacterSkill)
class CharacterSkillAdmin(admin.ModelAdmin):
    list_display = ['character', 'skill', 'skill_level']
    list_filter = ['skill_level', 'created_at']
    search_fields = ['character__name', 'skill__name']