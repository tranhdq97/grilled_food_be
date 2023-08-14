from base.common.constant.db_fields import CommonFields, TableFields


class TableListQueryFields:
    SEARCH_FIELDS = (CommonFields.NAME,)
    ORDER_FIELDS = (
        CommonFields.ID,
        CommonFields.NAME,
    )
    ORDER_DEFAULT_FIELD = f"{CommonFields.NAME}"
    FILTERSET_FIELDS = (CommonFields.NAME, TableFields.IS_AVAILABLE)
