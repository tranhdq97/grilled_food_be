from base.common.utils.utils import BaseEnum


class CommonFields(str, BaseEnum):
    PK = "pk"
    ID = "id"
    USER = "user"
    NAME = "name"
    TYPE = "type"
    TYPE_ID = "type_id"
    IS_DELETED = "is_deleted"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    CREATED_BY = "created_by"
    CREATED_BY_ID = "created_by_id"
    UPDATED_BY = "updated_by"
    UPDATED_BY_ID = "updated_by_id"


class MasterFields(str, BaseEnum):
    PARENT_ID = "parent_id"
    NAME = "name"


class MasterCountryFields(str, BaseEnum):
    CODE = "code"


class MasterCityFields(str, BaseEnum):
    COUNTRY = "country"
    COUNTRY_ID = "country_id"


class MasterDistrictFields(str, BaseEnum):
    CITY = "city"
    CITY_ID = "city_id"
    ZIP_CODE = "zipcode"


class AddressFields(str, BaseEnum):
    DISTRICT = "district"
    DISTRICT_ID = "district_id"
    STREET = "street"


class ProfileFields(str, BaseEnum):
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    DOB = "dob"
    PHONE_NUMBER = "phone_number"
    SEX = "sex"
    SEX_ID = "sex_id"
    ADDRESS = "address"
    ADDRESS_ID = "address_id"
    CITIZEN_NUMBER = "citizen_number"


class UserFields(str, BaseEnum):
    PROFILE = "profile"
    PROFILE_ID = "profile_id"
    EMAIL = "email"
    PASSWORD = "password"
    NEW_PASSWORD = "new_password"
    IS_ACTIVATE = "is_activate"
    IS_LEAVE = "is_leave"
    IS_ADMIN = "is_admin"
    LAST_LOGIN = "last_login"


class ItemFields(str, BaseEnum):
    PRICE = "price"


class TableFields(str, BaseEnum):
    IN_TABLE_STAFF = "in_table_staff"
    IN_TABLE_STAFF_ID = "in_table_staff_id"
    IS_AVAILABLE = "is_available"


class OrderFields(str, BaseEnum):
    TABLE = "table"
    TABLE_ID = "table_id"
    PAID_AT = "paid_at"
    NUM_PEOPLE = "num_people"
    ORDER_ITEMS = "order_items"


class OrderItemFields(str, BaseEnum):
    ORDER = "order"
    ORDER_ID = "order_id"
    ITEM = "item"
    ITEM_ID = "item_id"
    QUANTITY = "quantity"
