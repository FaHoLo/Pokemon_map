# Generated by Django 2.2.3 on 2019-09-24 21:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_auto_20190925_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='next_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_evo', to='pokemon_entities.Pokemon'),
        ),
    ]