import uuid
from django.db import models
from django.conf import settings


class Session(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("ARCHIVED", "Archived"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    master = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="master_sessions"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    # system_key removido - agora os personagens usam RPGSystem

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sessão"
        verbose_name_plural = "Sessões"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.master.username} ({self.get_status_display()})"


class SessionMember(models.Model):
    ROLE_CHOICES = [
        ("MASTER", "Mestre"),
        ("PLAYER", "Jogador"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="members"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "user")
        verbose_name = "Membro da Sessão"
        verbose_name_plural = "Membros das Sessões"
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.session.name} ({self.get_role_display()})"


class SessionInvite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="invites"
    )

    code = models.CharField(max_length=20, unique=True)

    max_uses = models.IntegerField(null=True, blank=True)
    uses_count = models.IntegerField(default=0)

    expires_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Convite de Sessão"
        verbose_name_plural = "Convites de Sessão"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Convite {self.code} - {self.session.name}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        if self.expires_at and timezone.now() > self.expires_at:
            return False
        if self.max_uses and self.uses_count >= self.max_uses:
            return False
        return True


class SessionCharacter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="session_characters"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    character = models.ForeignKey(
        "characters.Character",
        on_delete=models.PROTECT
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("session", "user")