from base.common.utils.utils import BaseEnum


class DBTable(str, BaseEnum):
    # Master tables
    MASTER = "master"
    MASTER_COUNTRY = "m_country"
    MASTER_CITY = "m_city"
    MASTER_DISTRICT = "m_district"
    MASTER_SEX = "m_sex"
    MASTER_STAFF_TYPE = "m_staff_type"
    MASTER_ITEM_TYPE = "m_item_type"
    ADDRESS = "address"
    PROFILE = "profile"
    STAFF = "staff"
    TABLE = "table"
    ORDER = "order"
    ORDER_ITEM = "order_item"
    ITEM = "item"
