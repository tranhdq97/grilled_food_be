from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import IsSuperStaff, IsApproved
from base.common.constant import message
from base.common.constant.view_action import BaseViewAction, OrderExtraViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied, APIErr
from base.order.models import Order
from staff.order.filters.order import OrderListQueryFields
from staff.order.serializers.order import (
    OrderListSlz,
    OrderRetrieveSlz,
    OrderCreateSlz,
    OrderUpdateSlz,
    OrderBulkUpdateSlz,
)


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    serializer_class = OrderListSlz
    queryset = Order.objects.filter(paid_at__isnull=True)
    search_fields = OrderListQueryFields.SEARCH_FIELDS
    ordering_fields = OrderListQueryFields.ORDER_FIELDS
    ordering = OrderListQueryFields.ORDER_DEFAULT_FIELD
    filterset_fields = OrderListQueryFields.FILTERSET_FIELDS

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.LIST: OrderListSlz,
            BaseViewAction.RETRIEVE: OrderRetrieveSlz,
            BaseViewAction.CREATE: OrderCreateSlz,
            BaseViewAction.UPDATE: OrderUpdateSlz,
            OrderExtraViewAction.ORDER: OrderBulkUpdateSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.LIST: (IsApproved,),
            BaseViewAction.RETRIEVE: (IsApproved,),
            BaseViewAction.CREATE: (IsApproved,),
            BaseViewAction.UPDATE: (IsApproved,),
            BaseViewAction.DESTROY: (IsSuperStaff,),
            OrderExtraViewAction.ORDER: (IsApproved,),
        }
        self.permission_classes = perm_switcher.get(
            self.action, self.permission_classes
        )
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()

    def order(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            raise APIErr(detail=message.INVALID_INPUT)
        slz = self.get_serializer(instance=instance, data=request.data)
        slz.is_valid(raise_exception=True)
        slz.save()
        return Response(data=slz.data)
