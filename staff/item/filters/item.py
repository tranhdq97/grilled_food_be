from base.common.constant.db_fields import CommonFields, ItemFields


class ItemListQueryFields:
    SEARCH_FIELDS = (CommonFields.NAME,)
    ORDER_FIELDS = (
        CommonFields.ID,
        ItemFields.PRICE,
        CommonFields.NAME,
    )
    ORDER_DEFAULT_FIELD = f"{CommonFields.NAME}"
    FILTERSET_FIELDS = (CommonFields.NAME, CommonFields.TYPE_ID)
