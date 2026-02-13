import uuid
from django.db import models

class SessionMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    session = models.ForeignKey(
        "session.Session",
        on_delete=models.CASCADE,
        related_name="maps"
    )

    name = models.CharField(max_length=120)
    image_url = models.URLField(blank=True, null=True)  # depois você troca por storage/file
    grid_enabled = models.BooleanField(default=True)
    grid_size = models.IntegerField(default=50)

    width = models.IntegerField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)