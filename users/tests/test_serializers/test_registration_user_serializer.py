from django.test import TestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ...models import User
from ...serializers.RegistrationUserSerializer import \
    RegistrationUserSerializer


class RegistrationUserSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RegistrationUserSerializer

        cls.user = User.objects.create_user(**{
            'phone_number': '7' * 11,
            'email': 'test@test.test',
            'password': 'password',
        })

    def test_Should_InheritTokenObtainPairSerializer(self):
        expected_super_classes = (
            TokenObtainPairSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_OverrideSuperMethods(self):
        expected_methods = [
            TokenObtainPairSerializer.validate,
        ]
        real_methods = [
            self.tested_class.validate,
        ]

        self.assertNotEquals(expected_methods, real_methods)

    def test_When_SetUserAsInstance_Should_CreateTokens(self):
        instance = self.user

        serializer = self.tested_class(instance=instance, data={
            'phone_number': 'phone_number',
            'password': 'password',
        })
        serializer.is_valid(raise_exception=True)

        expected_data_keys = (
            'refresh', 'access',
        )
        real_data_keys = tuple(serializer.validated_data.keys())

        self.assertEqual(expected_data_keys, real_data_keys)
