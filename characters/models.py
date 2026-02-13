import uuid
from django.conf import settings
from django.db import models

class Character(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters"
    )

    player_name = models.CharField(max_length=120, blank=True, null=True)  # "Jogador"
    name = models.CharField(max_length=120)                                # "Personagem"
    system_key = models.CharField(max_length=30, default="EPICORPG")

    xp_total = models.IntegerField(default=0)
    portrait_url = models.URLField(blank=True, null=True)

    sheet_data = models.JSONField(default=dict)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Personagem"
        verbose_name_plural = "Personagens"
    
    def __str__(self):
        player_info = f" ({self.player_name})" if self.player_name else ""
        return f"{self.name}{player_info} - {self.system_key}"