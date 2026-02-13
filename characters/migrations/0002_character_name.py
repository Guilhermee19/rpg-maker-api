# Generated manually - adding name field to Character model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=120, default='Personagem'),
        ),
    ]