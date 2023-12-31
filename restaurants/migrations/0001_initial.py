# Generated by Django 4.2.4 on 2023-08-27 16:46

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(help_text='Human readable address', max_length=255)),
                ('geo_position', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('coverage_area', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
    ]
