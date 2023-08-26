from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase

from ...models import User
from ...serializers.LoginUserSerializer import LoginUserSerializer
from ...views.LoginUserView import LoginUserView


class LoginUserViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LoginUserView
        cls.serializer = LoginUserSerializer
        cls.url = reverse('signin')

        User.objects.create_user(**{
            'phone_number': '7' * 11,
            'email': 'test@test.test',
            'password': 'password',
        })

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

    def test_When_PostMethod_Should_ErrorWithStatus400(self):
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

    def test_When_PostMethodWithNotValidData_Should_ReturnErrorAndStatus401(
            self,
    ):
        data = {
            'username': 'user@test.test',
            'password': 'password',
        }
        response = self.client.post(self.url, data)

        expected_status = status.HTTP_401_UNAUTHORIZED
        real_status = response.status_code

        expected_data = {
            'detail': 'No active account found with the given credentials',
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostMethodWithEmail_Should_ReturnTokensAndStatus200(self):
        data = {
            'username': 'test@test.test',
            'password': 'password',
        }

        url = self.url
        response = self.client.post(url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data_keys = ['refresh', 'access']
        real_data_keys = list(response.data.keys())

        tokens_value = response.data.values()
        tokens_is_empty = all([token.isspace() for token in tokens_value])

        expected_cookie = {
            'comment': '',
            'domain': '',
            'expires': '',
            'httponly': True,
            'max-age': '',
            'path': '/api/users/token',
            'samesite': 'strict',
            'secure': True,
            'version': '',
        }
        real_cookie = dict(response.cookies['refresh'])

        expected_refresh_cookie = response.data['refresh']
        real_refresh_cookie = response.cookies['refresh'].value

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data_keys, real_data_keys)
        self.assertFalse(tokens_is_empty)
        self.assertEqual(expected_cookie, real_cookie)
        self.assertEqual(expected_refresh_cookie, real_refresh_cookie)

    def test_When_PostMethodWithPhone_Should_ReturnTokensAndStatus200(self):
        data = {
            'username': '7' * 11,
            'password': 'password',
        }

        url = self.url
        response = self.client.post(url, data)

        expected_status = status.HTTP_200_OK
        real_status = response.status_code

        expected_data_keys = ['refresh', 'access']
        real_data_keys = list(response.data.keys())

        tokens_value = response.data.values()
        tokens_is_empty = all([token.isspace() for token in tokens_value])

        expected_cookie = {
            'comment': '',
            'domain': '',
            'expires': '',
            'httponly': True,
            'max-age': '',
            'path': '/api/users/token',
            'samesite': 'strict',
            'secure': True,
            'version': '',
        }
        real_cookie = dict(response.cookies['refresh'])

        expected_refresh_cookie = response.data['refresh']
        real_refresh_cookie = response.cookies['refresh'].value

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data_keys, real_data_keys)
        self.assertFalse(tokens_is_empty)
        self.assertEqual(expected_cookie, real_cookie)
        self.assertEqual(expected_refresh_cookie, real_refresh_cookie)
