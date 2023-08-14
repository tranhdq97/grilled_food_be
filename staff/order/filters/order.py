from base.common.constant.db_fields import (
    CommonFields,
    OrderFields,
)


class OrderListQueryFields:
    SEARCH_FIELDS = ("__".join([OrderFields.TABLE, CommonFields.NAME]),)
    ORDER_FIELDS = (
        "__".join([OrderFields.TABLE, CommonFields.NAME]),
        CommonFields.ID,
    )
    ORDER_DEFAULT_FIELD = f"{CommonFields.ID}"
    FILTERSET_FIELDS = (
        OrderFields.TABLE_ID,
        "__".join([OrderFields.TABLE, CommonFields.NAME]),
    )
