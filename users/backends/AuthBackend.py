from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()


class AuthBackend(ModelBackend):
    def authenticate(
            self, request, username=None, password=None, **kwargs,
    ) -> UserModel:
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is None or password is None:
            return None

        try:
            user = UserModel._default_manager.get(
                Q(email=username) | Q(phone_number=username),
            )
        except UserModel.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
