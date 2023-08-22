from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from base.address.models import Address
from base.auth.permissions.permission import (
    IsStaff,
    IsApproved,
    IsSuperStaff,
    IsManager,
)
from base.common.constant import message
from base.common.constant.view_action import BaseViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied, APIErr
from staff.address.filters.address import AddressListQueryFields
from staff.address.serializers.address import (
    AddressListSlz,
    AddressCreateSlz,
    AddressUpdateSlz,
    AddressRetrieveSlz,
)


class AddressViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    serializer_class = AddressListSlz
    queryset = Address.objects.all()
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = AddressListQueryFields.SEARCH_FIELDS
    ordering_fields = AddressListQueryFields.ORDER_FIELDS
    ordering = AddressListQueryFields.ORDER_DEFAULT_FIELD
    filterset_fields = AddressListQueryFields.FILTERSET_FIELDS

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.CREATE: AddressCreateSlz,
            BaseViewAction.UPDATE: AddressUpdateSlz,
            BaseViewAction.RETRIEVE: AddressRetrieveSlz,
            BaseViewAction.LIST: AddressListSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        if slz is None:
            raise APIErr(message.NO_SERIALIZER_MATCHED)

        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.CREATE: (IsStaff,),
            BaseViewAction.UPDATE: (IsApproved,),
            BaseViewAction.DESTROY: (IsManager | IsSuperStaff,),
            BaseViewAction.RETRIEVE: (IsStaff,),
            BaseViewAction.LIST: (IsStaff,),
        }
        self.permission_classes = perm_switcher.get(self.action, self.permission_classes)
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()
