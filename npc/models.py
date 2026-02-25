
from django.db import models
from django.conf import settings
from session.models import Session

class NPC(models.Model):
	HOSTILE = 'HOSTILE'
	FRIENDLY = 'FRIENDLY'
	NEUTRAL = 'NEUTRAL'
	MERCHANT = 'MERCHANT'
	TYPE_CHOICES = [
		(HOSTILE, 'Hostil'),
		(FRIENDLY, 'Amigável'),
		(NEUTRAL, 'Neutro'),
		(MERCHANT, 'Mercador'),
	]

	id = models.AutoField(primary_key=True)
	session = models.ForeignKey(
		Session,
		on_delete=models.CASCADE,
		related_name="npcs"
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="npcs"
	)
	type = models.CharField(max_length=10, choices=TYPE_CHOICES)
	name = models.CharField(max_length=200)
	picture = models.URLField(blank=True, null=True)
	life = models.IntegerField()
	note = models.TextField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "NPC"
		verbose_name_plural = "NPCs"
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.name} ({self.get_type_display()}) - {self.session.name}"
