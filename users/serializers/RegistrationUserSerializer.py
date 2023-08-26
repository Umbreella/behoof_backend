from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        refresh = self.get_token(self.instance)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
