from django.core.exceptions import ValidationError
from django.db.models import (BigAutoField, BooleanField, CharField,
                              DateTimeField, ManyToManyField, ManyToOneRel,
                              PositiveBigIntegerField)
from django.test import TestCase

from ...models import User


class UserModelTestCase(TestCase):
    databases = {'master', 'slave', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = User

        cls.data = {
            'first_name': 'q' * 50,
            'last_name': 'q' * 50,
            'phone_number': 7_900_000_00_01,
            'password': 'q' * 50,
        }

    def test_Should_IncludeRequiredFields(self):
        expected_fields = [
            'logentry', 'id', 'last_login', 'is_superuser', 'phone_number',
            'password', 'first_name', 'last_name', 'is_staff', 'is_active',
            'groups', 'user_permissions',
        ]
        real_fields = [
            field.name for field in self.tested_class._meta.get_fields()
        ]

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificTypeForEachField(self):
        expected_fields = {
            'logentry': ManyToOneRel,
            'id': BigAutoField,
            'last_login': DateTimeField,
            'is_superuser': BooleanField,
            'phone_number': PositiveBigIntegerField,
            'password': CharField,
            'first_name': CharField,
            'last_name': CharField,
            'is_staff': BooleanField,
            'is_active': BooleanField,
            'groups': ManyToManyField,
            'user_permissions': ManyToManyField,
        }
        real_fields = {
            field.name: field.__class__
            for field in self.tested_class._meta.get_fields()
        }

        self.assertEqual(expected_fields, real_fields)

    def test_Should_HelpTextForEachField(self):
        expected_help_text = {
            'logentry': '',
            'id': '',
            'last_login': '',
            'is_superuser': (
                'Designates that this user has all permissions without '
                'explicitly assigning them.'
            ),
            'phone_number': 'User`s unique phone number.',
            'password': 'User password.',
            'first_name': 'User`s name.',
            'last_name': 'User`s last name.',
            'is_staff': (
                'Does the user have access to the administration panel.'
            ),
            'is_active': 'Is this account active.',
            'groups': ''.join((
                'The groups this user belongs to. A user will get all ',
                'permissions granted to each of their groups.',
            )),
            'user_permissions': 'Specific permissions for this user.',
        }
        real_help_text = {
            field.name: (
                field.help_text if hasattr(field, 'help_text') else ''
            )
            for field in self.tested_class._meta.get_fields()
        }

        self.maxDiff = None

        self.assertEqual(expected_help_text, real_help_text)

    def test_When_CreateUserWithOutData_Should_ErrorBlankField(self):
        user = self.tested_class()

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'phone_number': [
                'This field cannot be null.',
            ],
            'password': [
                'This field cannot be blank.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_LengthDataGreaterThan128_Should_ErrorMaxLength(self):
        data = self.data
        data.update({
            'first_name': 'q' * 130,
            'last_name': 'q' * 130,
            'phone_number': 7_899_999_99_99,
            'password': 'q' * 130,
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'first_name': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
            'last_name': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
            'phone_number': [
                'Ensure this value is greater than or equal to 79000000000.',
            ],
            'password': [
                'Ensure this value has at most 128 characters (it has 130).',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_EmailIsNotValid_Should_ErrorInvalidValue(self):
        data = self.data
        data.update({
            'phone_number': 8_000_000_00_01,
        })

        user = self.tested_class(**data)

        with self.assertRaises(ValidationError) as _raise:
            user.save()

        expected_raise = {
            'phone_number': [
                'Ensure this value is less than or equal to 80000000000.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)

    def test_When_AllDataIsValid_Should_SaveUserAndReturnFullNameAsStr(self):
        data = self.data

        user = self.tested_class(**data)
        user.save()

        expected_str = f'{user.first_name} {user.last_name}'
        real_str = str(user)

        self.assertEqual(expected_str, real_str)

    def test_When_NamesIsNull_Should_ReturnEmailAsFullName(self):
        data = self.data
        data.pop('first_name')
        data.pop('last_name')

        user = self.tested_class(**data)
        user.save()

        expected_str = f'{user.phone_number}'
        real_str = str(user)

        self.assertEqual(expected_str, real_str)

    def test_When_DuplicateUserEmail_Should_ErrorDuplicateUser(self):
        data = self.data

        user = self.tested_class(**data)
        user.save()

        duplicate_user = User(**data)

        with self.assertRaises(ValidationError) as _raise:
            duplicate_user.save()

        expected_raise = {
            'phone_number': [
                'User with this Phone number already exists.',
            ],
        }
        real_raise = _raise.exception.message_dict

        self.assertEqual(expected_raise, real_raise)
