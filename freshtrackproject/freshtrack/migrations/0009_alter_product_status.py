# Generated by Django 5.0.4 on 2024-05-04 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshtrack', '0008_shoppinglist_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Opened', 'Opened')], max_length=100),
        ),
    ]
