# Generated by Django 5.1.3 on 2024-11-17 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_booksmodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booksmodel',
            name='category',
            field=models.CharField(choices=[('fiction', 'Fiction'), ('non_fiction', 'Non-Fiction'), ('romance', 'Romance'), ('classic', 'Classic'), ('dystopian', 'Dystopian Fiction'), ('historical', 'Historical Fiction'), ('biography', 'Biography'), ('mystery', 'Mystery'), ('science_fiction', 'Science Fiction'), ('fantasy', 'Fantasy')], max_length=50),
        ),
        migrations.AlterField(
            model_name='booksmodel',
            name='summary',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='booksmodel',
            name='year',
            field=models.IntegerField(),
        ),
    ]
