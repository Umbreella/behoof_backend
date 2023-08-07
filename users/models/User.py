import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .UserManager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.PositiveBigIntegerField(**{
        'unique': True,
        'validators': (
            MinValueValidator(7_900_000_00_00),
            MaxValueValidator(8_000_000_00_00),
        ),
        'help_text': 'User`s unique phone number.',
    })
    password = models.CharField(**{
        'max_length': 128,
        'help_text': 'User password.',
    })
    first_name = models.CharField(**{
        'max_length': 128,
        'blank': True,
        'help_text': 'User`s name.',
    })
    last_name = models.CharField(**{
        'max_length': 128,
        'blank': True,
        'help_text': 'User`s last name.',
    })
    is_staff = models.BooleanField(**{
        'default': False,
        'help_text': 'Does the user have access to the administration panel.',
    })
    is_active = models.BooleanField(**{
        'default': False,
        'help_text': 'Is this account active.',
    })

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ()

    objects = UserManager()

    def __str__(self) -> str:
        fullname = f'{self.first_name} {self.last_name}'

        if len(fullname) > 1:
            return fullname

        return f'{self.phone_number}'

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)

        phone_number_is_not_unique = User.objects.using('master').filter(**{
            'phone_number': self.phone_number,
        }).exists()

        if phone_number_is_not_unique:
            raise ValidationError({
                'phone_number': [
                    'User with this Phone number already exists.'
                ],
            })

    def save(self, *args, **kwargs) -> None:
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()

        self.full_clean()

        current_password = self.password
        hashed_password_pattern = self.__get_hashed_pattern()

        if not re.fullmatch(hashed_password_pattern, current_password):
            self.set_password(current_password)

        super().save(*args, **kwargs)

    def __get_hashed_pattern(self) -> str:
        hash_algorithms = {
            'PBKDF2PasswordHasher': r'\w+[$]\d+[$]\w+[$].+',
            'MD5PasswordHasher': r'\w+[$]\w+[$].+',
        }

        password_hasher = settings.PASSWORD_HASHERS[0].split('.')[-1]
        current_hash = hash_algorithms.get(password_hasher)

        assert current_hash is not None, 'Not found password hasher'

        return current_hash
