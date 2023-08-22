from django_filters import FilterSet

from base.common.constant.db_fields import (
    CommonFields,
    OrderFields,
    OrderItemFields,
)
from base.order_item.models import OrderItem


class OrderItemListQueryFields:
    SEARCH_FIELDS = ()
    ORDER_FIELDS = (
        "__".join([OrderItemFields.ITEM, CommonFields.NAME]),
        CommonFields.ID,
    )
    ORDER_DEFAULT_FIELD = "__".join([OrderItemFields.ITEM, CommonFields.NAME])
    FILTERSET_FIELDS = "__".join([OrderItemFields.ORDER, OrderFields.TABLE_ID])


class OrderItemFilter(FilterSet):
    class Meta:
        model = OrderItem
        fields = ()
