from django.db import models
from django.db.models import ForeignKey

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_fields import MasterFields, MasterCityFields
from base.common.constant.db_table import DBTable
from base.common.models.base import MasterBaseModel
from base.master.models.country import MasterCountry


class MasterCity(MasterBaseModel):
    name = models.CharField(max_length=32, unique=False)
    country = ForeignKey(MasterCountry, on_delete=models.RESTRICT, related_name=DBTable.MASTER_CITY)

    class Meta:
        db_table = DBTable.MASTER_CITY
        app_label = ModelAppLabel.MASTER
        unique_together = [MasterFields.NAME, MasterCityFields.COUNTRY]

    def __str__(self):
        return self.name
