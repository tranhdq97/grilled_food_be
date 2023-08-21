from django.db import models
from django.db.models import ForeignKey

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import DateTimeModel, Creator, Editor
from base.item.models import Item
from base.order.models.order import Order


class OrderItem(DateTimeModel, Creator, Editor):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name=DBTable.ORDER_ITEM)
    item = ForeignKey(Item, on_delete=models.RESTRICT, related_name=DBTable.ITEM)
    quantity = models.IntegerField()

    class Meta:
        db_table = DBTable.ORDER_ITEM
        app_label = ModelAppLabel.ORDER_ITEM
