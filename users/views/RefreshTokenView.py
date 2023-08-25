from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from ..utils import replace_refresh_token_from_cookie


class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        replace_refresh_token_from_cookie(request)

        is_oauth_token = False

        response = TokenRefreshView.post(self, request, *args, **kwargs)

        if is_oauth_token:
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
