# Generated by Django 5.1.3 on 2024-11-17 14:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_author_remove_booksmodel_author_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='registration_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
