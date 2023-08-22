from base.common.utils.utils import BaseEnum


class ModelAppLabel(str, BaseEnum):
    MASTER = "master"
    PROFILE = "profile"
    STAFF = "staff"
    CUSTOMER = "customer"
    FILE_MANAGEMENT = "file_management"
    ITEM = "item"
    ORDER = "order"
    ORDER_ITEM = "order_item"
    ADDRESS = "address"
    TABLE = "table"
