from typing import List, Set
from django.db import transaction
from rest_framework import serializers

from base.common.constant import message
from base.common.constant.db_fields import CommonFields, OrderFields, OrderItemFields
from base.common.utils.exceptions import APIErr
from base.common.utils.serializer import ForeignKeyField
from base.order.models import Order
from base.order_item.models import OrderItem
from base.table.models import Table
from staff.order_item.serializers.order_item import OrderItemUpdateSlz
from staff.table.serializers.table import TableRetrieveSlz, TableListSlz


class OrderBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            CommonFields.ID,
            CommonFields.UPDATED_AT,
        )


class OrderCreateSlz(OrderBaseSlz):
    table_id = ForeignKeyField(Table, write_only=True)
    order_items = OrderItemUpdateSlz(many=True, required=True, write_only=True)

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (
            OrderFields.TABLE_ID,
            OrderFields.ORDER_ITEMS,
        )

    def create(self, validated_data):
        table_id = validated_data.get(OrderFields.TABLE_ID, 0)
        table = Table.objects.filter(id=table_id).first()
        if table and not table.is_available:
            raise APIErr(message.NOT_AVAILABLE)
        order, _ = Order.objects.get_or_create(table_id=table_id, paid_at__isnull=True)
        return self._create_order_items(validated_data, order.id)

    def _create_order_items(
        self, validated_data: dict, order_id: int
    ) -> List[OrderItem]:
        order_item_data = validated_data.get(OrderFields.ORDER_ITEMS, [])
        if not order_item_data:
            raise APIErr(detail=message.INVALID_INPUT)
        with transaction.atomic():
            item_ids = set(
                order_item.get(OrderItemFields.ITEM_ID, 0)
                for order_item in order_item_data
            )
            order_item_dict = {
                x: order_item
                for order_item in order_item_data
                if (x := order_item.get(OrderItemFields.ITEM_ID, 0)) > 0
            }
            existed_order_items = list(
                OrderItem.objects.filter(order_id=order_id, item_id__in=item_ids)
            )
            new_item_ids = item_ids.difference(
                set([order_item.item_id for order_item in existed_order_items])
            )
            created_order_items = self._create_new_order_items(
                order_item_dict=order_item_dict,
                order_id=order_id,
                item_ids=new_item_ids,
            )
            updated_order_items = self._update_order_items(
                order_item_dict=order_item_dict, order_items=existed_order_items
            )
            order_items = created_order_items + updated_order_items
        return order_items

    def _create_new_order_items(
        self, order_item_dict: dict, order_id: int, item_ids: Set[int]
    ) -> List[OrderItem]:
        created_order_items = []
        for _id in item_ids:
            data = order_item_dict.pop(_id, {})
            data[OrderItemFields.ORDER_ID] = order_id
            created_order_items.append(OrderItem(**data))
        if created_order_items:
            created_order_items = OrderItem.objects.bulk_create(created_order_items)
        return created_order_items

    def _update_order_items(self, order_item_dict: dict, order_items: List[OrderItem]):
        updated_order_items = []
        for order_item in order_items:
            data = order_item_dict.pop(order_item.item.id, {})
            order_item.quantity += data.get(OrderItemFields.QUANTITY, 0)
            updated_order_items.append(order_item)
        if updated_order_items:
            OrderItem.objects.bulk_update(
                updated_order_items, fields=[OrderItemFields.QUANTITY]
            )
        return updated_order_items


class OrderUpdateSlz(OrderBaseSlz):
    table_id = ForeignKeyField(Table, required=False, write_only=True)

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (
            OrderFields.PAID_AT,
            OrderFields.NUM_PEOPLE,
            OrderFields.TABLE_ID,
        )
        extra_kwargs = {OrderFields.NUM_PEOPLE: {"required": False}}

    def update(self, instance, validated_data):
        paid_at = validated_data.get(OrderFields.PAID_AT, None)
        if paid_at:
            instance.table.is_available = True
            instance.table.save()
        return super().update(instance, validated_data)


class OrderRetrieveSlz(OrderBaseSlz):
    table = TableRetrieveSlz()

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (
            OrderFields.PAID_AT,
            OrderFields.NUM_PEOPLE,
            OrderFields.TABLE,
        )


class OrderListSlz(OrderBaseSlz):
    table = TableListSlz()

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (
            OrderFields.PAID_AT,
            OrderFields.NUM_PEOPLE,
            OrderFields.TABLE,
        )


class OrderBulkUpdateSlz(OrderBaseSlz):
    order_items = OrderItemUpdateSlz(many=True, required=True)

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (OrderFields.ORDER_ITEMS,)

    def update(self, instance, validated_data):
        order_item_data = validated_data.get(OrderFields.ORDER_ITEMS, [])
        if not order_item_data:
            raise APIErr(detail=message.INVALID_INPUT)
        with transaction.atomic():
            item_ids = set(
                order_item.get(OrderItemFields.ITEM_ID, 0)
                for order_item in order_item_data
            )
            order_item_dict = {
                x: order_item
                for order_item in order_item_data
                if (x := order_item.get(OrderItemFields.ITEM_ID, 0)) > 0
            }
            existed_order_items = OrderItem.objects.filter(
                order_id=instance.id, item_id__in=item_ids
            )
            new_item_ids = item_ids.difference(
                set(existed_order_items.values_list(OrderItemFields.ITEM_ID, flat=True))
            )
            created_order_items = self.create_order_items(
                order_item_dict=order_item_dict,
                order_id=instance.id,
                item_ids=new_item_ids,
            )
            updated_order_items = self.update_order_items(
                order_item_dict=order_item_dict, order_items=existed_order_items
            )
            order_items = created_order_items + updated_order_items
            instance.order_items = order_items
        return instance

    @staticmethod
    def create_order_items(
        order_item_dict: dict, order_id: int, item_ids: Set[int]
    ) -> List[OrderItem]:
        created_order_items = []
        for _id in item_ids:
            data = order_item_dict.pop(_id, {})
            data[OrderItemFields.ORDER_ID] = order_id
            created_order_items.append(OrderItem(**data))
        if created_order_items:
            OrderItem.objects.bulk_create(created_order_items)
        return created_order_items

    def update_order_items(self, order_item_dict: dict, order_items: List[OrderItem]):
        updated_order_items = []
        for order_item in order_items:
            data = order_item_dict.pop(order_item.item.id, {})
            order_item.quantity += data.get(OrderItemFields.QUANTITY, 0)
            updated_order_items.append(order_item)
        if updated_order_items:
            OrderItem.objects.bulk_update(
                updated_order_items, fields=[OrderItemFields.QUANTITY]
            )
        return updated_order_items

    @staticmethod
    def single_update(instance: OrderItem, data: dict):
        for key, value in data.items():
            if key == OrderItemFields.ITEM_ID:
                continue
            setattr(instance, key, value)
        return instance
