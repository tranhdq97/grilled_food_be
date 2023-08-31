from django.db import models

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import DateTimeModel, Creator, Editor
from base.staff.models import Staff


class Table(DateTimeModel, Creator, Editor):
    name = models.CharField(max_length=32)
    is_available = models.BooleanField(default=True)
    in_table_staff = models.ForeignKey(
        Staff, on_delete=models.RESTRICT, related_name=DBTable.TABLE, null=True
    )

    class Meta:
        db_table = DBTable.TABLE
        app_label = ModelAppLabel.TABLE
