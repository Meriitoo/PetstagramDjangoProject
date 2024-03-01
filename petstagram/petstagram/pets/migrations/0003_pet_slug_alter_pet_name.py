# Generated by Django 5.0.1 on 2024-01-24 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_create_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='slug',
            field=models.SlugField(default='none', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pet',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]