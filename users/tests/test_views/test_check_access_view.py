from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.test import APITestCase

from ...models import User
from ...views.CheckAccessView import CheckAccessView


class CheckAccessViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = CheckAccessView
        cls.serializer = Serializer
        cls.url = reverse('token_check')

        cls.user = User.objects.create_user(**{
            'phone_number': '7' * 11,
            'email': 'test@test.test',
            'password': 'password',
        })

    def test_Should_PermissionClassesIsAllowAny(self):
        expected_permission_classes = (
            IsAuthenticated,
        )
        real_permission_classes = self.tested_class.permission_classes

        self.assertEqual(expected_permission_classes, real_permission_classes)

    def test_Should_SerializerClassIsLoginUserSerializer(self):
        expected_serializer = self.serializer
        real_serializer = self.tested_class.serializer_class

        self.assertEqual(expected_serializer, real_serializer)

    def test_When_PathMethod_Should_ErrorWithStatus405(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PutMethod_Should_ErrorWithStatus405(self):
        self.client.force_authenticate(self.user)

        response = self.client.put(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_PatchMethod_Should_ErrorWithStatus405(self):
        self.client.force_authenticate(self.user)

        response = self.client.patch(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_DeleteMethod_Should_ErrorWithStatus405(self):
        self.client.force_authenticate(self.user)

        response = self.client.delete(self.url)

        expected_status = status.HTTP_405_METHOD_NOT_ALLOWED
        real_status = response.status_code

        self.assertEqual(expected_status, real_status)

    def test_When_GetMethod_Should_ReturnEmptyDataWithStatus200(self):
        self.client.force_authenticate(self.user)

        response = self.client.get(self.url)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data = {}
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)
