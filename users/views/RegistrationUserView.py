from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from ..serializers.RegistrationUserSerializer import RegistrationUserSerializer
from ..serializers.UserProfileSerializer import UserProfileSerializer


class RegistrationUserView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        data = request.data

        user_serializer = self.serializer_class(data=data)
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()

        token_serializer = RegistrationUserSerializer(user, data={
            f'{RegistrationUserSerializer.username_field}': 'username_field',
            'password': 'password',
        })
        token_serializer.is_valid(raise_exception=True)

        response = Response()

        response.status_code = status.HTTP_201_CREATED
        response.data = token_serializer.validated_data

        response.set_cookie(**{
            'key': 'refresh',
            'value': response.data['refresh'],
            'path': '/api/users/token/',
            'domain': None,
            'secure': True,
            'httponly': True,
            'samesite': 'strict',
        })

        return response
