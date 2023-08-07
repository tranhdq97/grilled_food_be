from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from base.auth.permissions.permission import IsManager, IsSuperStaff
from base.common.constant.db_fields import CommonFields, MasterFields
from base.common.constant.db_table import DBTable
from base.common.constant.service import Master
from base.common.constant.view_action import BaseViewAction
from base.common.custom.pagination import CustomPagination
from base.common.utils.exceptions import PermissionDenied
from base.master.filters.base import BaseMasterListQueryFields
from base.master.serializers.base import (
    MasterBaseListReqParams,
    MasterBaseSlz,
    MasterBaseCreateSlz,
)
from base.master.services.base import MasterBaseService


class MasterViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    pagination_class = CustomPagination
    serializer_class = MasterBaseSlz
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    search_fields = BaseMasterListQueryFields.SEARCH_FIELDS
    ordering_fields = BaseMasterListQueryFields.ORDER_FIELDS
    ordering = BaseMasterListQueryFields.ORDER_DEFAULT_FIELD

    def get_serializer_class(self) -> Serializer:
        slz_switcher = {
            BaseViewAction.CREATE: MasterBaseCreateSlz,
            BaseViewAction.LIST: MasterBaseSlz,
        }
        return slz_switcher.get(self.action, self.serializer_class)

    def get_permissions(self):
        perm_switcher = {
            BaseViewAction.LIST: (AllowAny,),
            BaseViewAction.DESTROY: (IsSuperStaff | IsManager,),
            BaseViewAction.CREATE: (IsSuperStaff | IsManager,),
        }
        self.permission_classes = perm_switcher.get(
            self.action, self.permission_classes
        )
        if self.permission_classes is None:
            raise PermissionDenied()
        return super().get_permissions()

    @extend_schema(
        description=f'Choices: {" | ".join(Master.list(allowed_to_create=False))}'
    )
    def destroy(self, request, *args, **kwargs):
        master_name = kwargs.pop("_".join([DBTable.MASTER, MasterFields.NAME]))
        pk = kwargs.pop(CommonFields.ID)
        service = MasterBaseService(master_name)
        service.delete(pk)
        return Response(status=200)

    @extend_schema(
        parameters=[MasterBaseListReqParams],
        description=f'Choices: {" | ".join(Master.list(allowed_to_create=False))}',
    )
    def list(self, request, **kwargs):
        master_name = kwargs.pop("_".join([DBTable.MASTER, MasterFields.NAME]))
        ordering = request.query_params.get("ordering", self.ordering)
        service = MasterBaseService(master_name)
        qs = service.list(parent_id=request.query_params.get(MasterFields.PARENT_ID))
        qs = qs.order_by(ordering)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = service.slz(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = service.slz(qs, many=True)
        return Response(serializer.data)

    @extend_schema(
        description=f'Choices: {" | ".join(Master.list(allowed_to_create=True))}'
    )
    def create(self, request, **kwargs):
        master_name = kwargs.pop("_".join([DBTable.MASTER, MasterFields.NAME]))
        service = MasterBaseService(master_name)
        res = service.create(request.data)
        return Response(res.data)
