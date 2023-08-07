from django.db import models
from django.db.models import ForeignKey

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_fields import MasterFields, MasterDistrictFields
from base.common.constant.db_table import DBTable
from base.common.models.base import MasterBaseModel
from base.master.models.city import MasterCity


class MasterDistrict(MasterBaseModel):
    name = models.CharField(max_length=32, unique=False)
    city = ForeignKey(
        MasterCity, on_delete=models.RESTRICT, related_name=DBTable.MASTER_DISTRICT
    )
    zipcode = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = DBTable.MASTER_DISTRICT
        app_label = ModelAppLabel.MASTER
        unique_together = [MasterFields.NAME, MasterDistrictFields.CITY]
