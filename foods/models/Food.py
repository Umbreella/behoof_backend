from django.db import models

from .Category import Category


class Food(models.Model):
    category = models.ForeignKey(**{
        'to': Category,
        'null': True,
        'on_delete': models.SET_NULL,
        'related_name': 'foods',
        'help_text': 'Food category.',
    })

    preview = models.ImageField(**{
        'upload_to': 'food/%Y/%m/%d/',
        'help_text': 'Food preview.',
    })
    title = models.CharField(**{
        'max_length': 255,
        'help_text': 'Food title.',
    })
    composition = models.TextField(**{
        'help_text': 'Composition of the food.',
    })
    description = models.TextField(**{
        'help_text': 'Food description.',
    })
    price = models.DecimalField(**{
        'max_digits': 10,
        'decimal_places': 2,
        'help_text': 'Food price',
    })
    weight = models.PositiveIntegerField(**{
        'help_text': 'Food weight in grams.',
    })

    proteins = models.DecimalField(**{
        'max_digits': 6,
        'decimal_places': 1,
        'help_text': 'Amount of proteins.',
    })
    fats = models.DecimalField(**{
        'max_digits': 6,
        'decimal_places': 1,
        'help_text': 'Amount of fats.',
    })
    carbohydrates = models.DecimalField(**{
        'max_digits': 6,
        'decimal_places': 1,
        'help_text': 'Amount of carbohydrates.',
    })
    kilocalories = models.PositiveIntegerField(**{
        'help_text': 'Amount of kilocalories.',
    })

    is_published = models.BooleanField(**{
        'default': False,
        'help_text': 'Displayed to the user.',
    })

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        if self.price:
            self.price = round(self.price, 2)

        if self.proteins:
            self.proteins = round(self.proteins, 1)

        if self.fats:
            self.fats = round(self.fats, 1)

        if self.carbohydrates:
            self.carbohydrates = round(self.carbohydrates, 1)

        self.full_clean()
        super().save(*args, *kwargs)
