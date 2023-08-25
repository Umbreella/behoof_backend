from django.test import TestCase

from ...models import User
from ...models.UserManager import UserManager


class UserManagerTestCase(TestCase):
    databases = {'master', 'slave', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserManager()
        cls.tested_class.model = User

        cls.data = {
            'phone_number': '7' * 11,
            'password': 'user',
        }

    def test_When_CallCreateUser_Should_CreateSimpleUser(self):
        data = self.data
        user = self.tested_class.create_user(**data)

        expected_is_staff = False
        real_is_staff = user.is_staff

        expected_is_superuser = False
        real_is_superuser = user.is_superuser

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)

    def test_When_CallCreateSuperUserWithIsStaffFalse_Should_ErrorIsStaff(
            self):
        data = self.data
        data.update({
            'is_staff': False,
        })

        with self.assertRaises(ValueError) as _raise:
            self.tested_class.create_superuser(**data)

        expected_raise = 'Superuser must have is_staff=True.'
        real_raise = str(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_CallCreateSuperUserWithIsSuperFalse_Should_ErrorIsSuper(
            self):
        data = self.data
        data.update({
            'is_superuser': False,
        })

        with self.assertRaises(ValueError) as _raise:
            self.tested_class.create_superuser(**data)

        expected_raise = 'Superuser must have is_superuser=True.'
        real_raise = str(_raise.exception)

        self.assertEqual(expected_raise, real_raise)

    def test_When_CallCreateSuperUser_Should_CreateAdminUser(self):
        data = self.data

        user = self.tested_class.create_superuser(**data)

        expected_is_staff = True
        real_is_staff = user.is_staff

        expected_is_superuser = True
        real_is_superuser = user.is_superuser

        self.assertEqual(expected_is_staff, real_is_staff)
        self.assertEqual(expected_is_superuser, real_is_superuser)
