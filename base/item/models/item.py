from django.db import models

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_fields import CommonFields
from base.common.constant.db_table import DBTable
from base.common.models.base import Creator, Editor, DateTimeModel
from base.master.models import MasterItemType


class Item(DateTimeModel, Creator, Editor):
    name = models.CharField(max_length=10)
    type = models.ForeignKey(
        MasterItemType, on_delete=models.RESTRICT, related_name=DBTable.ITEM
    )
    price = models.IntegerField()

    class Meta:
        unique_together = ((CommonFields.NAME, CommonFields.TYPE_ID),)
        db_table = DBTable.ITEM
        app_label = ModelAppLabel.ITEM
