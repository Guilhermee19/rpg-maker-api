from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel


class CharacterClass(TimeStampedModel):
    """RPG Character Classes (Warrior, Mage, Archer, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    base_health = models.PositiveIntegerField(default=100)
    base_mana = models.PositiveIntegerField(default=50)
    base_attack = models.PositiveIntegerField(default=10)
    base_defense = models.PositiveIntegerField(default=5)
    base_speed = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return self.name


class Character(TimeStampedModel):
    """Player Characters"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=100)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)
    experience = models.PositiveIntegerField(default=0)
    
    # Current Stats
    current_health = models.PositiveIntegerField(default=100)
    current_mana = models.PositiveIntegerField(default=50)
    
    # Calculated Stats
    @property
    def max_health(self):
        return self.character_class.base_health + (self.level * 10)
    
    @property
    def max_mana(self):
        return self.character_class.base_mana + (self.level * 5)
    
    @property
    def attack(self):
        return self.character_class.base_attack + (self.level * 2)
    
    @property
    def defense(self):
        return self.character_class.base_defense + (self.level * 1)
    
    @property
    def speed(self):
        return self.character_class.base_speed + (self.level * 1)
    
    def __str__(self):
        return f'{self.name} ({self.character_class.name}) - Level {self.level}'


class ItemType(models.TextChoices):
    WEAPON = 'weapon', 'Weapon'
    ARMOR = 'armor', 'Armor'
    CONSUMABLE = 'consumable', 'Consumable'
    ACCESSORY = 'accessory', 'Accessory'
    MISC = 'misc', 'Miscellaneous'


class Item(TimeStampedModel):
    """Game Items"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    value = models.PositiveIntegerField(default=0)  # Gold value
    rarity = models.CharField(max_length=20, choices=[
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary')
    ], default='common')
    
    # Stat modifiers
    health_bonus = models.IntegerField(default=0)
    mana_bonus = models.IntegerField(default=0)
    attack_bonus = models.IntegerField(default=0)
    defense_bonus = models.IntegerField(default=0)
    speed_bonus = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.name} ({self.get_rarity_display()})'


class CharacterItem(TimeStampedModel):
    """Character's inventory"""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_equipped = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['character', 'item']
    
    def __str__(self):
        return f'{self.character.name} - {self.item.name} x{self.quantity}'


class Skill(TimeStampedModel):
    """Character Skills/Abilities"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    mana_cost = models.PositiveIntegerField(default=0)
    cooldown = models.PositiveIntegerField(default=0)  # in turns/seconds
    damage = models.PositiveIntegerField(default=0)
    healing = models.PositiveIntegerField(default=0)
    required_level = models.PositiveIntegerField(default=1)
    character_classes = models.ManyToManyField(CharacterClass, related_name='skills')
    
    def __str__(self):
        return self.name


class CharacterSkill(TimeStampedModel):
    """Character's learned skills"""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_level = models.PositiveIntegerField(default=1)
    
    class Meta:
        unique_together = ['character', 'skill']
    
    def __str__(self):
        return f'{self.character.name} - {self.skill.name} (Level {self.skill_level})'