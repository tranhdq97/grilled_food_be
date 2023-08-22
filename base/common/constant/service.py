from base.common.constant.db_table import DBTable

from base.common.constant import message
from base.common.utils.exceptions import APIErr
from base.common.utils.utils import BaseEnum


class Master(BaseEnum):
    # table_name, model_name, allowed_to_create
    m_sex = DBTable.MASTER_SEX, "MasterSex", False
    m_city = DBTable.MASTER_CITY, "MasterCity", False
    m_country = DBTable.MASTER_COUNTRY, "MasterCountry", False
    m_district = DBTable.MASTER_DISTRICT, "MasterDistrict", False
    m_item_type = DBTable.MASTER_ITEM_TYPE, "MasterItemType", False
    m_staff_type = DBTable.MASTER_STAFF_TYPE, "MasterStaffType", False

    @staticmethod
    def list(allowed_to_create: bool = False) -> list:
        master_list = list(filter(lambda c: (allowed_to_create is False or c.value[2]), Master))
        return [x.value[0].value for x in master_list]

    @staticmethod
    def unpack(master_name: str) -> tuple:
        master = list(filter(lambda c: c.value[0] == master_name, Master))
        if not master:
            raise APIErr(message.NOT_EXIST)

        return master[0].value
