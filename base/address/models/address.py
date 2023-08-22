from django.db import models
from django.db.models import ForeignKey

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import DateTimeModel
from base.master.models import MasterDistrict


class Address(DateTimeModel):
    district = ForeignKey(MasterDistrict, on_delete=models.RESTRICT, related_name=DBTable.MASTER_DISTRICT)
    street = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = DBTable.ADDRESS
        app_label = ModelAppLabel.ADDRESS
