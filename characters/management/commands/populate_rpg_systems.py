from django.core.management.base import BaseCommand
from characters.models import RPGSystem

class Command(BaseCommand):
    help = 'Popula sistemas de RPG padrão'

    def handle(self, *args, **options):
        self.stdout.write("=== Populando Sistemas de RPG ===")
        
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
            self.stdout.write(self.style.SUCCESS('✅ D&D 5e criado como sistema padrão'))
        else:
            dnd5e.is_default = True
            dnd5e.save()
            self.stdout.write(self.style.SUCCESS('✅ D&D 5e definido como padrão'))
        
        # Sistema genérico (compatibilidade)
        generic_data = {
            "basic_info": {"level": 1, "class": "", "race": ""},
            "attributes": {"strength": 10, "dexterity": 10, "constitution": 10, "intelligence": 10, "wisdom": 10, "charisma": 10},
            "derived_stats": {"hit_points": {"max": 10, "current": 10}, "armor_class": 10},
            "notes": {"backstory": "", "appearance": ""}
        }
        
        generic, created = RPGSystem.objects.get_or_create(
            slug='generic',
            defaults={
                'name': 'Sistema Genérico',
                'description': 'Sistema básico para qualquer tipo de RPG',
                'base_sheet_data': generic_data,
                'is_default': False,
                'is_active': True
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('✅ Sistema Genérico criado'))
        
        # Call of Cthulhu
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
                "charm": 15,
                "climb": 20,
                "credit_rating": 0,
                "cthulhu_mythos": 0,
                "dodge": 25,
                "drive_auto": 20,
                "fast_talk": 5,
                "fight_brawl": 25,
                "first_aid": 30,
                "history": 5,
                "intimidate": 15,
                "jump": 20,
                "library_use": 20,
                "listen": 20,
                "medicine": 1,
                "occult": 5,
                "persuade": 10,
                "psychology": 10,
                "spot_hidden": 25,
                "stealth": 20,
                "swim": 20
            },
            "equipment": {
                "weapons": [],
                "items": []
            },
            "notes": {
                "backstory": "",
                "appearance": "",
                "personality": ""
            }
        }
        
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
            self.stdout.write(self.style.SUCCESS('✅ Call of Cthulhu criado'))
        
        total = RPGSystem.objects.count()
        self.stdout.write(f"=== Total de sistemas: {total} ===")
        
        for system in RPGSystem.objects.all():
            status = "📌 PADRÃO" if system.is_default else "⭐ ATIVO" if system.is_active else "💤 INATIVO"
            self.stdout.write(f"{status} {system.name} ({system.slug})")