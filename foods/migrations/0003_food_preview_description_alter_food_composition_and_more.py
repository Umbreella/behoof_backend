# Generated by Django 4.2.5 on 2023-09-15 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_alter_food_kilocalories'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='preview_description',
            field=models.CharField(default='', help_text='Food short description.', max_length=255),
        ),
        migrations.AlterField(
            model_name='food',
            name='composition',
            field=models.TextField(default='', help_text='Composition of the food.'),
        ),
        migrations.AlterField(
            model_name='food',
            name='description',
            field=models.TextField(default='', help_text='Food description.'),
        ),
        migrations.AlterField(
            model_name='food',
            name='title',
            field=models.CharField(default='', help_text='Food title.', max_length=255),
        ),
    ]
