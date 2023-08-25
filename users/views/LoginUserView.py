from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers.LoginUserSerializer import LoginUserSerializer


class LoginUserView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        response.set_cookie(**{
            'key': 'refresh',
            'value': response.data['refresh'],
            'path': '/api/users/token',
            'domain': None,
            'secure': True,
            'httponly': True,
            'samesite': 'strict',
        })

        return response
