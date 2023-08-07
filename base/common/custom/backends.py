from django.contrib.auth.backends import BaseBackend

from base.common.constant import message
from base.common.utils.exceptions import APIErr
from base.staff.models import Staff


class ModelBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if request is None:
            return

        username = kwargs.get(Staff.USERNAME_FIELD)
        password = kwargs.get("password")
        if not username or not password:
            return

        try:
            user = Staff._default_manager.get_by_natural_key(username)
        except Staff.DoesNotExist:
            raise APIErr(message.EMAIL_OR_PASSWORD_IS_INCORRECT)
        else:
            return self.validate_user(user, password)

    def validate_user(self, user, password):
        if not user.check_password(password):
            raise APIErr(message.EMAIL_OR_PASSWORD_IS_INCORRECT)

        # TODO: Check verifying status of email
        return user
