import uuid
import json
import os
from django.conf import settings
from django.db import models


def get_default_sheet_data():
    """Retorna o template padrão da ficha de personagem"""
    template_path = os.path.join(settings.BASE_DIR, 'character_sheet_template.json')
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback básico caso o arquivo não exista
        return {
            "basic_info": {"level": 1, "class": "", "race": ""},
            "attributes": {"strength": 10, "dexterity": 10, "constitution": 10, "intelligence": 10, "wisdom": 10, "charisma": 10},
            "derived_stats": {"hit_points": {"max": 10, "current": 10}, "armor_class": 10},
            "notes": {"backstory": "", "appearance": ""}
        }

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters"
    )

    player_name = models.CharField(max_length=120, blank=True, null=True)  # "Jogador"
    name = models.CharField(max_length=120, default="Personagem")  # "Nome do Personagem"
    avatar_url = models.URLField(blank=True, null=True)
    system_key = models.CharField(max_length=30, default="EPICORPG")
    xp_total = models.IntegerField(default=0)

    sheet_data = models.JSONField(default=get_default_sheet_data)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Personagem"
        verbose_name_plural = "Personagens"
    
    def __str__(self):
        player_info = f" ({self.player_name})" if self.player_name else ""
        return f"{self.player_name}{player_info} - {self.system_key}"