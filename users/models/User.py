import re

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CheckConstraint, Q
from phonenumber_field.modelfields import PhoneNumberField

from .UserManager import UserManager


class User(AbstractUser):
    email = models.EmailField(**{
        'unique': True,
        'blank': True,
        'help_text': 'User`s unique email address.',
    })
    phone_number = PhoneNumberField(**{
        'unique': True,
        'blank': True,
        'max_length': 16,
        'help_text': 'User`s unique phone number.',
    })
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('phone_number',)

    objects = UserManager()

    class Meta:
        constraints = [
            CheckConstraint(check=Q(email__isnull=False) | Q(
                phone_number__isnull=False), name='or_email_or_phone'),
        ]

    def __str__(self):
        return f'{self.phone_number}'

    def password_is_hashed(self):
        return bool(re.fullmatch(r'\w+[$]\d+[$]\w+[$].+', self.password))

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.password and not self.password_is_hashed():
            self.set_password(self.password)

        super().save(*args, **kwargs)
