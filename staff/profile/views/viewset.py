from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import (
    IsStaff,
    IsSuperStaff,
    IsManager,
)
from base.common.constant import message
from base.common.constant.view_action import BaseViewAction
from base.common.utils.exceptions import PermissionDenied, APIErr
from base.profile.models import Profile
from staff.profile.serializers.profile import (
    ProfileRetrieveSlz,
)


class ProfileViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    serializer_class = ProfileRetrieveSlz
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.RETRIEVE: ProfileRetrieveSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        if slz is None:
            raise APIErr(message.NO_SERIALIZER_MATCHED)

        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.DESTROY: (IsManager | IsSuperStaff,),
            BaseViewAction.RETRIEVE: (IsStaff,),
        }
        self.permission_classes = perm_switcher.get(
            self.action, self.permission_classes
        )
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()
