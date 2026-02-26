from django.db import models


class Item(models.Model):
    session = models.ForeignKey(
        "session.Session",
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=255)
    image = models.URLField(blank=True)
    category = models.CharField(max_length=100)
    durability_current = models.FloatField()
    durability_max = models.FloatField()
    rarity = models.CharField(max_length=100)
    effects = models.JSONField(blank=True, null=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.name