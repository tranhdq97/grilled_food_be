from base.common.utils.utils import BaseEnum


class MasterStaffTypeID(int, BaseEnum):
    SUPER_STAFF = 1
    MANAGER = 2
    EMPLOYEE = 3
    UNAPPROVED = 4


class MasterFilterByID(int, BaseEnum):
    TODAY = 1
    THIS_MONTH = 2
    THIS_YEAR = 3
    LAST_FIVE_YEARS = 4
