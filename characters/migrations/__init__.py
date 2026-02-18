# Migration para popular sistemas de RPG padrão

from django.db import migrations

def populate_default_systems(apps, schema_editor):
    """Popula sistemas de RPG padrão"""
    RPGSystem = apps.get_model('characters', 'RPGSystem')
        
    # Sistema Epico RPG (Padrão)
    epicRPG_data = {
        "player_name": "Ekko",
        "system_key": "EPICORPG",
        "xp_total": 0,
        "avatar_url": None,
        "sheet_data": {
            "attributes": {
                "vigor": {
                    "value": 5,
                    "xp": 0,
                    "fatigue": 0
                },
                "agility": {
                    "value": 5,
                    "xp": 0,
                    "fatigue": 0
                },
                "intelligence": {
                    "value": 5,
                    "xp": 0,
                    "fatigue": 0
                }
            },
            "secondary": {
                "difficulty_target": 12,
                "willpower": {
                    "value": 5,
                    "xp": 0
                },
                "damage_bonus": 3,
                "perception": {
                    "value": 5,
                    "xp": 0
                },
                "speed": 5,
                "size": {
                    "value": "MEDIO"
                },
                "hit_points": {
                    "value": 10,
                    "xp": 0,
                    "hurt": 0
                },
                "wounds": 0,
                "carry": {
                    "heavy": 25,
                    "min": 75,
                    "max": 100
                }
            },
            "aptitudes": [],
            "virtues": [],
            "defects": [],
            "skills": [],
            "attacks": [],
            "armors": [],
            "money_treasures": [],
            "items_equipment": [],
            "notes": ""
        },
        "is_active": True
    }
    
    RPGSystem.objects.get_or_create(
        slug='epicRPG',
        defaults={
            'name': 'Épico RPG',
            'description': 'Épico RPG é um jogo de interpretação para jogos épicos em qualquer cenário ou gênero de aventura.',
            'base_sheet_data': epicRPG_data,
            'is_default': True,
            'is_active': True
        }
    )


    # Sistema D&D 5e (Padrão)
    dnd5e_data = {
        "basic_info": {
            "level": 1,
            "class": "",
            "race": "",
            "background": "",
            "alignment": ""
        },
        "attributes": {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10
        },
        "derived_stats": {
            "hit_points": {
                "max": 10,
                "current": 10,
                "temporary": 0
            },
            "armor_class": 10,
            "speed": 30,
            "proficiency_bonus": 2
        },
        "skills": {
            "acrobatics": 0,
            "animal_handling": 0,
            "arcana": 0,
            "athletics": 0,
            "deception": 0,
            "history": 0,
            "insight": 0,
            "intimidation": 0,
            "investigation": 0,
            "medicine": 0,
            "nature": 0,
            "perception": 0,
            "performance": 0,
            "persuasion": 0,
            "religion": 0,
            "sleight_of_hand": 0,
            "stealth": 0,
            "survival": 0
        },
        "equipment": {
            "weapons": [],
            "armor": [],
            "items": []
        },
        "spells": {
            "spell_slots": {},
            "known_spells": []
        },
        "notes": {
            "backstory": "",
            "appearance": "",
            "personality": "",
            "ideals": "",
            "bonds": "",
            "flaws": ""
        }
    }
    
    # D&D 5e (Sistema padrão)
    RPGSystem.objects.get_or_create(
        slug='dnd5e',
        defaults={
            'name': 'D&D 5ª Edição',
            'description': 'Sistema oficial de Dungeons & Dragons 5ª edição',
            'base_sheet_data': dnd5e_data,
            'is_default': False,
            'is_active': True
        }
    )

def reverse_populate_systems(apps, schema_editor):
    """Remove sistemas padrão"""
    RPGSystem = apps.get_model('characters', 'RPGSystem')
    RPGSystem.objects.filter(slug__in=['dnd5e', 'epicRPG']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_add_rpg_system'),
    ]

    operations = [
        migrations.RunPython(
            populate_default_systems,
            reverse_populate_systems
        ),
    ]