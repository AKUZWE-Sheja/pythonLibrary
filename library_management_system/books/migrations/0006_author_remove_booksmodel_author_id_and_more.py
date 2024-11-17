# Generated by Django 5.1.3 on 2024-11-17 14:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_alter_booksmodel_category_alter_booksmodel_summary_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('registration_date', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'authors',
                'ordering': ['name'],
            },
        ),
        migrations.RemoveField(
            model_name='booksmodel',
            name='author_id',
        ),
        migrations.AlterField(
            model_name='booksmodel',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='books.author'),
        ),
    ]
