from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base.common.constant import message
from base.common.constant.constant import RegexPattern
from base.common.constant.db_fields import CommonFields, UserFields
from base.common.utils.exceptions import APIErr
from base.common.utils.strings import check_regex


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT default serializer"""

    def get_token(self, user):
        token = super().get_token(user)
        return token

    def validate(self, attrs):
        attrs = super().validate(attrs)
        refresh = self.get_token(self.user)
        attrs["access"] = str(refresh.access_token)
        attrs["refresh"] = str(refresh)
        return attrs


class ForgetPasswordSlz(serializers.Serializer):
    # TODO: Send an email helping user change password
    pass


class ChangePasswordSlz(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        user = self.context.get(CommonFields.USER)
        if not check_regex(RegexPattern.PASSWORD, new_password):
            raise APIErr(message.PASSWORD_FAILED)

        if new_password == user.email:
            raise APIErr(message.PASSWORD_IDENTICAL_AS_EMAIL)

        return new_password

    def validate_old_password(self, old_password):
        user = self.context.get(CommonFields.USER)
        if not user.check_password(old_password):
            raise APIErr(message.PASSWORD_DID_NOT_MATCH)

        return old_password

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get(UserFields.NEW_PASSWORD))
        instance.save()
        return instance
