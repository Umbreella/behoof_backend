# Generated by Django 4.2.4 on 2023-08-28 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='kilocalories',
            field=models.DecimalField(decimal_places=1, help_text='Amount of kilocalories.', max_digits=6),
        ),
    ]
