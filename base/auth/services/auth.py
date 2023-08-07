import logging

from base.auth.serializers.auth import ChangePasswordSlz
from base.common.constant import message
from base.common.utils.decorator import log
from base.staff.serializers.staff import StaffRetrieveSlz

logger = logging.getLogger(__name__)


class AuthSvc:
    @staticmethod
    @log
    def change_password(user, data):
        slz = ChangePasswordSlz(data=data, context=dict(user=user))
        slz.is_valid(raise_exception=True)
        slz.update(user, data)
        return dict(massage=message.PASSWORD_CHANGE_SUCCESSFUL)

    @staticmethod
    @log
    def get_me(user):
        slz = StaffRetrieveSlz(user)
        return slz.data
