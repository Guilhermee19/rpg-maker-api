import hashlib
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    EXPIRY_HOURS = 2

    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'

    def is_valid(self):
        if self.used:
            return False
        expiry = self.created_at + timedelta(hours=self.EXPIRY_HOURS)
        return timezone.now() < expiry

    @staticmethod
    def generate_token(user):
        """Invalida tokens anteriores e gera um novo"""
        PasswordResetToken.objects.filter(user=user, used=False).update(used=True)

        raw = f"{user.pk}{user.email}{os.urandom(32).hex()}"
        token = hashlib.sha256(raw.encode()).hexdigest()

        return PasswordResetToken.objects.create(user=user, token=token)