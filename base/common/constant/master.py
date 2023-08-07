from base.common.utils.utils import BaseEnum


class MasterStaffTypeID(int, BaseEnum):
    SUPER_STAFF = 1
    MANAGER = 2
    EMPLOYEE = 3
    UNAPPROVED = 4

    @classmethod
    def is_manager_or_super_staff(cls, staff_type: int) -> bool:
        return staff_type in (cls.MANAGER, cls.SUPER_STAFF)


class MasterFilterByID(int, BaseEnum):
    TODAY = 1
    THIS_MONTH = 2
    THIS_YEAR = 3
    LAST_FIVE_YEARS = 4
