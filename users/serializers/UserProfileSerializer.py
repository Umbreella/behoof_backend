from django.core.exceptions import ValidationError as DjValidationError
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import User


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(max_length=254, required=True)
    phone_number = PhoneNumberField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email', 'phone_number', 'password',
        )

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except DjValidationError as ex:
            raise ValidationError(ex.message_dict)
