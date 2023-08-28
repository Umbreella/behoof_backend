from django.contrib.gis.db import models


class Restaurant(models.Model):
    address = models.CharField(**{
        'max_length': 255,
        'help_text': 'Human readable address.',
    })
    geo_position = models.PointField()
    coverage_area = models.PolygonField()

    def __str__(self):
        return f'{self.address}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
