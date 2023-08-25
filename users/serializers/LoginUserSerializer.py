from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginUserSerializer(TokenObtainPairSerializer):
    username_field = 'username'
