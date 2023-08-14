from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import IsSuperStaff, IsManager, IsApproved
from base.common.constant.view_action import BaseViewAction, TableExtraViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied
from base.table.models import Table
from staff.table.filters.table import TableListQueryFields
from staff.table.serializers.table import (
    TableListSlz,
    TableRetrieveSlz,
    TableCreateSlz,
    TableUpdateSlz,
    TableUpdateStaffInOutSlz,
)


class TableViewSet(
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
    serializer_class = TableListSlz
    queryset = Table.objects.all()
    search_fields = TableListQueryFields.SEARCH_FIELDS
    ordering_fields = TableListQueryFields.ORDER_FIELDS
    ordering = TableListQueryFields.ORDER_DEFAULT_FIELD
    filterset_fields = TableListQueryFields.FILTERSET_FIELDS

    def get_serializer_class(self):
        slz_switcher = {
            BaseViewAction.LIST: TableListSlz,
            BaseViewAction.RETRIEVE: TableRetrieveSlz,
            BaseViewAction.CREATE: TableCreateSlz,
            BaseViewAction.UPDATE: TableUpdateSlz,
            TableExtraViewAction.STAFF_IN: TableUpdateStaffInOutSlz,
            TableExtraViewAction.STAFF_OUT: TableUpdateStaffInOutSlz,
        }
        slz = slz_switcher.get(self.action, self.serializer_class)
        return slz

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.LIST: (IsApproved,),
            BaseViewAction.RETRIEVE: (IsApproved,),
            BaseViewAction.CREATE: (IsManager | IsSuperStaff,),
            BaseViewAction.UPDATE: (IsApproved,),
            BaseViewAction.DESTROY: (IsSuperStaff,),
            TableExtraViewAction.STAFF_IN: (IsApproved,),
        }
        self.permission_classes = perm_switcher.get(
            self.action, self.permission_classes
        )
        if self.permission_classes is None:
            raise PermissionDenied()

        return super().get_permissions()

    def update_staff_in(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.in_table_staff_id = self.request.user.id
        instance.save()
        slz = self.get_serializer(instance)
        return Response(data=slz.data)

    def update_staff_out(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.in_table_staff_id = None
        instance.save()
        slz = self.get_serializer(instance)
        return Response(data=slz.data)
