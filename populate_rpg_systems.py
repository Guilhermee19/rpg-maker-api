"""
Script para popular sistemas de RPG padrão
Execute com: python manage.py shell < populate_rpg_systems.py
"""

from characters.models import RPGSystem

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

# Sistema Pathfinder 2e
pathfinder_data = {
    "basic_info": {
        "level": 1,
        "class": "",
        "ancestry": "",
        "heritage": "",
        "background": ""
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
            "max": 8,
            "current": 8
        },
        "armor_class": 10,
        "speed": 25,
        "hero_points": 1
    },
    "saves": {
        "fortitude": 0,
        "reflex": 0,
        "will": 0
    },
    "skills": {},
    "feats": {
        "ancestry_feats": [],
        "class_feats": [],
        "general_feats": [],
        "skill_feats": []
    },
    "equipment": {
        "weapons": [],
        "armor": [],
        "items": []
    },
    "notes": {
        "backstory": "",
        "appearance": "",
        "personality": ""
    }
}

# Sistema Call of Cthulhu
coc_data = {
    "basic_info": {
        "age": 25,
        "occupation": "",
        "residence": "",
        "birthplace": ""
    },
    "attributes": {
        "strength": 50,
        "constitution": 50,
        "size": 50,
        "dexterity": 50,
        "appearance": 50,
        "intelligence": 50,
        "power": 50,
        "education": 50
    },
    "derived_stats": {
        "hit_points": 10,
        "sanity": 50,
        "luck": 50,
        "magic_points": 10
    },
    "skills": {
        "accounting": 5,
        "anthropology": 1,
        "appraise": 5,
        "archaeology": 1,
        "art_craft": 5,
        "charm": 15,
        "climb": 20,
        "credit_rating": 0,
        "cthulhu_mythos": 0,
        "disguise": 5,
        "dodge": 25,
        "drive_auto": 20,
        "electrical_repair": 10,
        "fast_talk": 5,
        "fight_brawl": 25,
        "firearms_handgun": 20,
        "firearms_rifle": 25,
        "first_aid": 30,
        "history": 5,
        "intimidate": 15,
        "jump": 20,
        "language_own": 0,
        "law": 5,
        "library_use": 20,
        "listen": 20,
        "locksmith": 1,
        "mechanical_repair": 10,
        "medicine": 1,
        "natural_world": 10,
        "navigate": 10,
        "occult": 5,
        "operate_heavy_machinery": 1,
        "persuade": 10,
        "pilot": 1,
        "psychology": 10,
        "psychoanalysis": 1,
        "ride": 5,
        "science": 1,
        "sleight_of_hand": 10,
        "spot_hidden": 25,
        "stealth": 20,
        "survival": 10,
        "swim": 20,
        "throw": 20,
        "track": 10
    },
    "equipment": {
        "weapons": [],
        "items": []
    },
    "notes": {
        "backstory": "",
        "appearance": "",
        "personality": "",
        "ideology": "",
        "significant_people": "",
        "meaningful_locations": "",
        "treasured_possessions": "",
        "traits": ""
    }
}

# Como usar este script manualmente
print("=== Populando Sistemas de RPG ===")

# D&D 5e (Sistema padrão)
dnd5e, created = RPGSystem.objects.get_or_create(
    slug='dnd5e',
    defaults={
        'name': 'D&D 5ª Edição',
        'description': 'Sistema oficial de Dungeons & Dragons 5ª edição',
        'base_sheet_data': dnd5e_data,
        'is_default': True,
        'is_active': True
    }
)
if created:
    print("✅ D&D 5e criado como sistema padrão")
else:
    dnd5e.is_default = True
    dnd5e.save()
    print("✅ D&D 5e definido como padrão")

# Pathfinder 2e
pathfinder, created = RPGSystem.objects.get_or_create(
    slug='pathfinder2e',
    defaults={
        'name': 'Pathfinder 2ª Edição',
        'description': 'Sistema Pathfinder 2ª edição da Paizo',
        'base_sheet_data': pathfinder_data,
        'is_default': False,
        'is_active': True
    }
)
if created:
    print("✅ Pathfinder 2e criado")

# Call of Cthulhu
coc, created = RPGSystem.objects.get_or_create(
    slug='call-of-cthulhu',
    defaults={
        'name': 'Call of Cthulhu',
        'description': 'Sistema de horror investigativo da Chaosium',
        'base_sheet_data': coc_data,
        'is_default': False,
        'is_active': True
    }
)
if created:
    print("✅ Call of Cthulhu criado")

# Sistema genérico (compatibilidade)
generic, created = RPGSystem.objects.get_or_create(
    slug='generic',
    defaults={
        'name': 'Sistema Genérico',
        'description': 'Sistema básico para qualquer tipo de RPG',
        'base_sheet_data': {
            "basic_info": {"level": 1, "class": "", "race": ""},
            "attributes": {"strength": 10, "dexterity": 10, "constitution": 10, "intelligence": 10, "wisdom": 10, "charisma": 10},
            "derived_stats": {"hit_points": {"max": 10, "current": 10}, "armor_class": 10},
            "notes": {"backstory": "", "appearance": ""}
        },
        'is_default': False,
        'is_active': True
    }
)
if created:
    print("✅ Sistema Genérico criado")

print(f"=== Total de sistemas: {RPGSystem.objects.count()} ===")
for system in RPGSystem.objects.all():
    status = "📌 PADRÃO" if system.is_default else "⭐ ATIVO" if system.is_active else "💤 INATIVO"
    print(f"{status} {system.name} ({system.slug})")