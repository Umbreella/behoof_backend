# Generated by Django 4.2.4 on 2023-08-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(help_text='Human readable address.', max_length=255),
        ),
    ]
