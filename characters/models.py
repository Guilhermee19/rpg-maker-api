import uuid
import json
import os
from django.conf import settings
from django.db import models
from django.utils.text import slugify


class RPGSystem(models.Model):
    """Modelo para diferentes sistemas de RPG"""
    
    slug = models.SlugField(max_length=100, unique=True, primary_key=True, editable=False)
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Template base para a ficha do personagem
    base_sheet_data = models.JSONField(default=dict)
    
    # Configurações do sistema
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sistema de RPG"
        verbose_name_plural = "Sistemas de RPG"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Garante que o slug seja a primary key e apenas um sistema seja o padrão"""
        if not self.slug:
            self.slug = slugify(self.name)
        
        if self.is_default:
            # Usa o slug (já gerado acima) em vez de self.pk,
            # pois self.pk é None em objetos novos e causaria erro no ORM
            RPGSystem.objects.exclude(slug=self.slug).update(is_default=False)

        super().save(*args, **kwargs)
    
    @classmethod
    def get_default_system(cls):
        """Retorna o sistema padrão"""
        return cls.objects.filter(is_default=True, is_active=True).first()
    
    @classmethod
    def get_default_sheet_data(cls, system_slug=None):
        """Retorna os dados base da ficha para um sistema específico ou o padrão"""
        if system_slug:
            try:
                system = cls.objects.get(slug=system_slug, is_active=True)
                if system.base_sheet_data:
                    return system.base_sheet_data
            except cls.DoesNotExist:
                pass
        
        # Fallback para sistema padrão
        default_system = cls.get_default_system()
        if default_system and default_system.base_sheet_data:
            return default_system.base_sheet_data  # corrigido: era default_system._data
        
        # Fallback final para dados básicos
        return {
            "basic_info": {
                "level": 1, 
                "class": "", 
                "race": ""
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
                    "current": 10
                },
                "armor_class": 10
            },
            "notes": {
                "backstory": "", 
                "appearance": ""
            }
        }


def get_default_sheet_data():
    """Retorna o template padrão da ficha de personagem baseado no sistema selecionado"""
    sheet_data = RPGSystem.get_default_sheet_data()
    if sheet_data:
        return sheet_data
    
    # Fallback para arquivo template (compatibilidade com versão anterior)
    template_path = os.path.join(settings.BASE_DIR, 'character_sheet_template.json')
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return RPGSystem.get_default_sheet_data()


class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters"
    )
    
    # Sistema de RPG utilizado
    rpg_system = models.ForeignKey(
        RPGSystem,
        on_delete=models.PROTECT,
        related_name="characters",
        null=True,
        blank=True,
        to_field='slug'
    )

    player_name = models.CharField(max_length=120, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    
    xp_total = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    sheet_data = models.JSONField(default=get_default_sheet_data)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Personagem"
        verbose_name_plural = "Personagens"
    
    def save(self, *args, **kwargs):
        """Override save to set default RPG system and apply sheet template"""
        # Se não tem sistema definido, usa o padrão
        if not self.rpg_system_id:
            self.rpg_system = RPGSystem.get_default_system()

        # Se é um novo personagem, sempre aplica o template do sistema
        if not self.pk:
            if self.rpg_system and self.rpg_system.base_sheet_data:
                self.sheet_data = self.rpg_system.base_sheet_data
            else:
                self.sheet_data = get_default_sheet_data()
        
        super().save(*args, **kwargs)
    
    @property
    def system_name(self):
        """Retorna o nome do sistema de RPG"""
        return self.rpg_system.name if self.rpg_system else "Sistema não definido"
    
    def __str__(self):
        player_info = f" ({self.player_name})" if self.player_name else ""
        system_name = self.rpg_system.name if self.rpg_system else "Sem sistema"
        return f"{self.player_name or 'Personagem'}{player_info} - {system_name}"