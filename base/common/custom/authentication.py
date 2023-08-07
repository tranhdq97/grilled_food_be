from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from rest_framework_simplejwt.authentication import JWTAuthentication

from base.staff.models import Staff


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        self.user_model = Staff
        user = super().get_user(validated_token)
        return user


class SimpleJWTTokenUserScheme(SimpleJWTScheme):
    target_class = CustomJWTAuthentication
