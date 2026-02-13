from django.db import models
from django.contrib.auth.models import User


class TimeStampedModel(models.Model):
    """Abstract base class with timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


# Profile removido - usando User padrão do Django para perfis