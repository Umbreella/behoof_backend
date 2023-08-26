from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...serializers.UserProfileSerializer import UserProfileSerializer
from ...views.RegistrationUserView import RegistrationUserView


class RegistrationUserViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = RegistrationUserView
        cls.serializer = UserProfileSerializer
        cls.url = reverse('signup')

        cls.data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'phone_number': '7' * 11,
            'email': 'test@test.test',
            'password': 'password',
        }

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            AllowAny,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsLoginUserSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_GetMethod_Should_ErrorWithStatus405(self):
        response = self.client.get(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        response = self.client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        response = self.client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PostMethodWithoutData_Should_ErrorWithStatus400(self):
        data = {}

        response = self.client.post(self.url, data)

        serializer = self.serializer(data=data)
        serializer.is_valid()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = serializer.errors
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodWithValidData_Should_ReturnTokensAndStatus201(
            self,
    ):
        data = self.data
        response = self.client.post(self.url, data)

        expected_status = status.HTTP_201_CREATED
        real_status = response.status_code

        expected_data_keys = (
            'refresh', 'access'
        )
        real_data_keys = tuple(response.data.keys())

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data_keys, real_data_keys)

    def test_When_PostMethodWithDuplicateData_Should_ReturnErrorWithStatus400(
            self,
    ):
        data = self.data
        self.client.post(self.url, data)

        response = self.client.post(self.url, data)

        serializer = self.serializer(data=data)
        serializer.is_valid()

        with self.assertRaises(ValidationError) as _raise:
            serializer.save()

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = _raise.exception.detail
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
