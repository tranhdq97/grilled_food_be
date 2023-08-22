from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import IsSuperStaff, IsApproved
from base.common.constant.view_action import BaseViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied
from base.order_item.models import OrderItem
from staff.order_item.filters.order_item import (
    OrderItemListQueryFields,
    OrderItemFilter,
)
from staff.order_item.serializers.order_item import (
    OrderItemListSlz,
    OrderItemRetrieveSlz,
)


class OrderItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = OrderItemListSlz
    queryset = OrderItem.objects.all()
    search_fields = OrderItemListQueryFields.SEARCH_FIELDS
    ordering_fields = OrderItemListQueryFields.ORDER_FIELDS
    ordering = OrderItemListQueryFields.ORDER_DEFAULT_FIELD
    filterset_fields = OrderItemListQueryFields.FILTERSET_FIELDS
    filterset_class = OrderItemFilter

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.LIST: OrderItemListSlz,
            BaseViewAction.RETRIEVE: OrderItemRetrieveSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.LIST: (IsApproved,),
            BaseViewAction.RETRIEVE: (IsApproved,),
            BaseViewAction.DESTROY: (IsSuperStaff,),
        }
        self.permission_classes = perm_switcher.get(self.action, self.permission_classes)
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()
