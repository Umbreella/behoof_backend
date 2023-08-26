from django.http import SimpleCookie
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.permissions import AllowAny
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

from ...models import User
from ...views.LogoutUserView import LogoutUserView


class LogoutUserViewTestCase(APITestCase):
    databases = {'master', }

    @classmethod
    def setUpTestData(cls):
        cls.tested_class = LogoutUserView
        cls.serializer = TokenBlacklistSerializer
        cls.url = reverse('token_destroy')

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
        response = self.client.post(self.url, {})

        expected_status = status.HTTP_400_BAD_REQUEST
        real_status = response.status_code

        expected_data = {
            'refresh': [
                ErrorDetail(**{
                    'string': 'This field is required.',
                    'code': 'required',
                }),
            ],
        }
        real_data = response.data

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_data, real_data)

    def test_When_PostWithRefreshInBody_Should_DestroyCookies(self):
        data_login = {
            'username': 'test@test.test',
            'password': 'password',
        }
        response_login = self.client.post(reverse('signin'), data_login)

        data = {
            'refresh': response_login.data.get('refresh'),
        }
        response = self.client.post(self.url, data)

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        expected_cookies = {
            'refresh': {
                'comment': '',
                'domain': '',
                'expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
                'httponly': '',
                'max-age': 0,
                'path': '/api/user/token',
                'samesite': 'strict',
                'secure': '',
                'version': '',
            },
        }
        real_cookies = dict(response.cookies)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_cookies, real_cookies)

    def test_When_PostWithRefreshInCookies_Should_DestroyCookies(self):
        data_login = {
            'username': 'test@test.test',
            'password': 'password',
        }
        response_login = self.client.post(reverse('signin'), data_login)

        self.client.cookies = SimpleCookie({
            'refresh': response_login.data.get('refresh'),
        })
        response = self.client.post(self.url, {})

        expected_status = status.HTTP_204_NO_CONTENT
        real_status = response.status_code

        expected_cookies = {
            'refresh': {
                'comment': '',
                'domain': '',
                'expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
                'httponly': '',
                'max-age': 0,
                'path': '/api/user/token',
                'samesite': 'strict',
                'secure': '',
                'version': '',
            },
        }
        real_cookies = dict(response.cookies)

        self.assertEqual(expected_status, real_status)
        self.assertEqual(expected_cookies, real_cookies)
