from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import BigAutoField, ManyToManyField, ManyToOneRel
from django.test import TestCase
from phonenumber_field.modelfields import PhoneNumberField

from ...models import User


class UserModelTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = User

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'phone_number': '7' * 11,
            'password': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'logentry', 'outstandingtoken', 'id', 'password', 'last_login',
            'is_superuser', 'first_name', 'last_name', 'is_staff', 'is_active',
            'date_joined', 'email', 'phone_number', 'groups',
            'user_permissions',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            **{
                field.name: field.__class__
                for field in AbstractUser._meta.get_fields()
            },
            'id': BigAutoField,
            'logentry': ManyToOneRel,
            'outstandingtoken': ManyToOneRel,
            'user_permissions': ManyToManyField,
            'phone_number': PhoneNumberField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        expected_fields.pop('username')

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            **{
                field.name: (
                    field.help_text if hasattr(field, 'help_text') else ''
                )
                for field in AbstractUser._meta.get_fields()
            },
            'id': '',
            'logentry': '',
            'outstandingtoken': '',
            'email': 'User`s unique email address.',
            'phone_number': 'User`s unique phone number.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        expected_help_text.pop('username')

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateInstanceWithOutData_Should_ErrorBlankField(self):
        instance = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            instance.save()

        expected_raise = {
            'password': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThanMaxLenght_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 255,
            'last_name': 'q' * 255,
            'email': 'q' * 245 + '@test.test',
            'password': 'q' * 255,
            'phone_number': '1' * 16,
        })

        instance = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            instance.save()

        expected_raise = {
            'first_name': [
                'Ensure this value has at most 150 characters (it has 255).',
            ],
            'last_name': [
                'Ensure this value has at most 150 characters (it has 255).',
            ],
            'email': [
                'Ensure this value has at most 254 characters (it has 255).',
            ],
            'phone_number': [
                'The phone number entered is not valid.',
            ],
            'password': [
                'Ensure this value has at most 128 characters (it has 255).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveUserAndReturnPhoneAsStr(self):
        data = self.data

        instance = self.tested_class(**data)
        instance.save()

        expected_str = f'{instance.phone_number}'
        real_str = str(instance)

        self.assertEqual(expected_str, real_str)

    def test_When_DuplicateUserEmail_Should_ErrorDuplicateUser(self):
        data = self.data

        instance = self.tested_class(**data)
        instance.save()

        duplicate_user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            duplicate_user.save()

        expected_raise = {
            'email': [
                'User with this Email already exists.',
            ],
            'phone_number': [
                'User with this Phone number already exists.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)
