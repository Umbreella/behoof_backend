from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(
            self, phone_number: int, password: str, **extra_fields,
    ):
        user = self.model(**{
            'phone_number': phone_number,
            'password': password,
            **extra_fields,
        })
        user.save()

        return user

    def create_user(
            self, phone_number: int = None, password: str = None,
            **extra_fields,
    ):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(
            self, phone_number: int = None, password: str = None,
            **extra_fields,
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)
