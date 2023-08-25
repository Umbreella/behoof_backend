from django.http import QueryDict
from rest_framework.request import Request


def replace_refresh_token_from_cookie(request: Request):
    if isinstance(request.data, QueryDict):
        request.data._mutable = True

    refresh = request.COOKIES.get('refresh', None)

    if refresh:
        request.data.update({
            'refresh': refresh,
        })
