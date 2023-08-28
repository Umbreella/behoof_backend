from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView

from ..utils import replace_refresh_token_from_cookie


class RefreshTokenView(TokenRefreshView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        replace_refresh_token_from_cookie(request)

        response = TokenRefreshView.post(self, request, *args, **kwargs)

        return response
