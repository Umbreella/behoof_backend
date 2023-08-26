from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.serializers import ModelSerializer
from snapshottest.django import TestCase

from ...models import User
from ...serializers.UserProfileSerializer import UserProfileSerializer


class UserProfileSerializerTestCase(TestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = UserProfileSerializer

    def test_Should_InheritModelSerializer(self):
        expected_super_classes = (
            ModelSerializer,
        )
        real_super_classes = self.tested_class.__bases__

        self.assertEqual(expected_super_classes, real_super_classes)

    def test_Should_IncludeDefiniteFieldsFromModel(self):
        expected_fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'password',
        ]
        real_fields = list(self.tested_class().get_fields())

        self.assertEqual(expected_fields, real_fields)

    def test_Should_SpecificFormatForEachField(self):
        real_repr = repr(self.tested_class())

        self.assertMatchSnapshot(real_repr)

    def test_Should_DontOverrideSuperMethods(self):
        expected_methods = [
            ModelSerializer.create,
            ModelSerializer.update,
        ]
        real_methods = [
            self.tested_class.create,
            self.tested_class.update,
        ]

        self.assertEqual(expected_methods, real_methods)

    def test_Should_OverrideSuperMethods(self):
        expected_methods = [
            ModelSerializer.save,
        ]
        real_methods = [
            self.tested_class.save,
        ]

        self.assertNotEquals(expected_methods, real_methods)

    def test_When_ValidationError_Should_ReturnDRFValidationError(self):
        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone_number': '7' * 11,
            'email': 'test@test.test',
            'password': 'password',
        }

        User.objects.create_user(**data)

        serializer = self.tested_class(data=data)
        serializer.is_valid(raise_exception=True)

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_raise = {
            'email': [
                ErrorDetail(**{
                    'string': 'User with this Email already exists.',
                    'code': 'invalid',
                }),
            ],
            'phone_number': [
                ErrorDetail(**{
                    'string': 'User with this Phone number already exists.',
                    'code': 'invalid',
                }),
            ],
        }

        real_raise = _raise.exception.detail

        self.assertEqual(expected_raise, real_raise)
