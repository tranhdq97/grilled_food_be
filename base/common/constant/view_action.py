from base.common.utils.utils import BaseEnum


class BaseViewAction(str, BaseEnum):
    LIST = "list"
    RETRIEVE = "retrieve"
    CREATE = "create"
    UPDATE = "update"
    DESTROY = "destroy"


class TableExtraViewAction(str, BaseEnum):
    STAFF_IN = "update_staff_in"
    STAFF_OUT = "update_staff_out"
