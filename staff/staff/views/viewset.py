from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import (
    IsStaff,
    IsSuperStaff,
    IsManager,
)
from base.common.constant import message
from base.common.constant.db_fields import CommonFields
from base.common.constant.master import MasterStaffTypeID
from base.common.constant.view_action import BaseViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied, APIErr
from base.staff.models import Staff
from base.staff.serializers.staff import StaffRetrieveSlz
from staff.staff.filters.staff import StaffListQueryFields
from staff.staff.serializers.staff import (
    StaffListSlz,
    StaffCreateSlz,
    StaffUpdateSlz,
)


class StaffViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    serializer_class = StaffListSlz
    queryset = Staff.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = StaffListQueryFields.SEARCH_FIELDS
    ordering_fields = StaffListQueryFields.ORDER_FIELDS
    ordering = StaffListQueryFields.ORDER_DEFAULT_FIELD
    filterset_fields = StaffListQueryFields.FILTERSET_FIELDS

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.CREATE: StaffCreateSlz,
            BaseViewAction.UPDATE: StaffUpdateSlz,
            BaseViewAction.RETRIEVE: StaffRetrieveSlz,
            BaseViewAction.LIST: StaffListSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        if slz is None:
            raise APIErr(message.NO_SERIALIZER_MATCHED)

        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.CREATE: (AllowAny,),
            BaseViewAction.UPDATE: (IsStaff,),
            BaseViewAction.RETRIEVE: (IsStaff,),
            BaseViewAction.LIST: (IsSuperStaff | IsManager,),
            BaseViewAction.DESTROY: (IsSuperStaff,),
        }
        self.permission_classes = perm_switcher.get(
            self.action, self.permission_classes
        )
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()

    @staticmethod
    def _validate_user(request, **kwargs):
        user = request.user
        current_user = user.id == kwargs.get(CommonFields.PK)
        is_manager = MasterStaffTypeID.is_manager_or_super_staff(
            staff_type=user.type_id
        )
        if not (current_user or is_manager):
            raise APIErr(message.PERMISSION_DENIED)

    def update(self, request, *args, **kwargs):
        self._validate_user(request=request, **kwargs)
        return super().update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self._validate_user(request=request, **kwargs)
        return super().retrieve(request, *args, **kwargs)
