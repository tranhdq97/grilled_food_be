from base.common.constant.db_fields import CommonFields, UserFields, ProfileFields


class StaffListQueryFields:
    SEARCH_FIELDS = (
        UserFields.EMAIL,
        "__".join([UserFields.PROFILE, ProfileFields.PHONE_NUMBER]),
        "__".join([UserFields.PROFILE, ProfileFields.FIRST_NAME]),
        "__".join([UserFields.PROFILE, ProfileFields.LAST_NAME]),
    )
    ORDER_FIELDS = (
        CommonFields.ID,
        UserFields.EMAIL,
        "__".join([UserFields.PROFILE, ProfileFields.FIRST_NAME]),
        "__".join([UserFields.PROFILE, ProfileFields.LAST_NAME]),
    )
    ORDER_DEFAULT_FIELD = f"{CommonFields.ID}"
    FILTERSET_FIELDS = (
        UserFields.EMAIL,
        "__".join([UserFields.PROFILE, ProfileFields.FIRST_NAME]),
        "__".join([UserFields.PROFILE, ProfileFields.LAST_NAME]),
        "__".join([UserFields.PROFILE, ProfileFields.PHONE_NUMBER]),
    )
