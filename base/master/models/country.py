from django.db import models

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import MasterBaseModel


class MasterCountry(MasterBaseModel):
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = DBTable.MASTER_COUNTRY
        app_label = ModelAppLabel.MASTER
