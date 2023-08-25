from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenBlacklistView

from ..utils import replace_refresh_token_from_cookie


class LogoutUserView(TokenBlacklistView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        replace_refresh_token_from_cookie(request)

        response = TokenBlacklistView.post(self, request, *args, **kwargs)

        response.status_code = status.HTTP_204_NO_CONTENT
        response.delete_cookie(**{
            'key': 'refresh',
            'path': '/api/user/token',
            'domain': None,
            'samesite': 'strict',
        })

        return response
