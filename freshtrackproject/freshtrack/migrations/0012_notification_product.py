# Generated by Django 5.0.4 on 2024-06-05 11:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshtrack', '0011_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='freshtrack.product'),
        ),
    ]
