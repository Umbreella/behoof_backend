from django.db import models


class Category(models.Model):
    title = models.CharField(**{
        'max_length': 255,
        'help_text': 'Category title.',
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
