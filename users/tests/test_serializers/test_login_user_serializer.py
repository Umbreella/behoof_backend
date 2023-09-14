from django.test import TestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...serializers.LoginUserSerializer import LoginUserSerializer


class LoginUserSerializerTestCase(TestCase):
    databases = {
        'master',
    }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LoginUserSerializer

    def test_Should_InheritTokenObtainPairSerializer(self):
        expected_super_classes = (
            TokenObtainPairSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_OverrideSuperUsernameField(self):
        expected_username_field = 'username'
        real_username_field = self.tested_class().username_field

        self.assertEqual(expected_username_field, real_username_field)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            TokenObtainPairSerializer.validate,
        ]
        real_methods = [
            self.tested_class.validate,
        ]

        self.assertEqual(expected_methods, real_methods)
