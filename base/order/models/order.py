from django.db import models
from django.db.models import ForeignKey

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import Editor, Creator, DateTimeModel
from base.table.models import Table


class Order(DateTimeModel, Creator, Editor):
    table = ForeignKey(Table, on_delete=models.RESTRICT, related_name=DBTable.ORDER)
    num_people = models.IntegerField(default=0)
    paid_at = models.DateTimeField(null=True)

    class Meta:
        db_table = DBTable.ORDER
        app_label = ModelAppLabel.ORDER
