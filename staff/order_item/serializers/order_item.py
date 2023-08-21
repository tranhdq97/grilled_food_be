from rest_framework import serializers

from base.common.constant import message
from base.common.constant.db_fields import CommonFields, OrderItemFields
from base.common.utils.exceptions import APIErr
from base.common.utils.serializer import ForeignKeyField
from base.item.models import Item
from base.order_item.models import OrderItem
from base.staff.serializers.staff import StaffRetrieveSlz
from staff.item.serializers.item import ItemRetrieveSlz, ItemListSlz


class OrderItemBaseSlz(serializers.ModelSerializer):
    def validate(self, attrs):
        quantity = self.instance and self.instance.quantity
        if quantity is not None and quantity < 1:
            raise APIErr(message.INVALID_INPUT)
        if quantity is not None:
            raise APIErr(message.INVALID_INPUT)

        return attrs

    class Meta:
        model = OrderItem
        fields = (
            CommonFields.ID,
            OrderItemFields.QUANTITY,
        )


class OrderItemCreateSlz(OrderItemBaseSlz):
    item_id = ForeignKeyField(Item, write_only=True)

    class Meta:
        model = OrderItemBaseSlz.Meta.model
        fields = OrderItemBaseSlz.Meta.fields + (OrderItemFields.ITEM_ID,)


class OrderItemUpdateSlz(OrderItemBaseSlz):
    item_id = ForeignKeyField(Item, required=False, write_only=True)

    class Meta:
        model = OrderItemBaseSlz.Meta.model
        fields = OrderItemBaseSlz.Meta.fields + (OrderItemFields.ITEM_ID,)
        extra_kwargs = {
            OrderItemFields.QUANTITY: {"required": False},
        }


class OrderItemRetrieveSlz(OrderItemBaseSlz):
    item = ItemRetrieveSlz()

    class Meta:
        model = OrderItemBaseSlz.Meta.model
        fields = OrderItemBaseSlz.Meta.fields + (OrderItemFields.ITEM,)


class OrderItemListSlz(OrderItemBaseSlz):
    item = ItemListSlz()

    class Meta:
        model = OrderItemBaseSlz.Meta.model
        fields = OrderItemBaseSlz.Meta.fields + (OrderItemFields.ITEM,)
