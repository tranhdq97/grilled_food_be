from base.common.constant.db_fields import (
    CommonFields,
    AddressFields,
    MasterDistrictFields,
)
from base.common.constant.db_table import DBTable


class AddressListQueryFields:
    SEARCH_FIELDS = (
        AddressFields.STREET,
        "__".join(
            (AddressFields.DISTRICT, MasterDistrictFields.ZIP_CODE),
        ),
    )
    ORDER_FIELDS = (
        CommonFields.ID,
        AddressFields.STREET,
    )
    ORDER_DEFAULT_FIELD = f"{CommonFields.ID}"
    FILTERSET_FIELDS = (AddressFields.DISTRICT_ID,)
