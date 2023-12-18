from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    preview = models.ImageField(**{
        'upload_to': 'promotion/%Y/%m/%d/',
        'help_text': 'Promotion preview.',
    })
    title = models.CharField(**{
        'max_length': 255,
        'help_text': 'Promotion title.',
    })
    description = models.TextField(**{
        'help_text': 'Promotion description.',
    })

    start_time = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Promotion start time.',
    })
    end_time = models.DateTimeField(**{
        'default': timezone.now,
        'help_text': 'Promotion start time.',
    })

    is_published = models.BooleanField(**{
        'default': False,
        'help_text': 'Displayed to the user.',
    })

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)
