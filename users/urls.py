from django.urls import path

from .views.CheckAccessView import CheckAccessView
from .views.LoginUserView import LoginUserView
from .views.LogoutUserView import LogoutUserView
from .views.RefreshTokenView import RefreshTokenView

urlpatterns = [
    path('signin/', LoginUserView.as_view(), name='signin'),

    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('token/destroy/', LogoutUserView.as_view(), name='token_destroy'),
    path('token/check/', CheckAccessView.as_view(), name='token_check'),
]
