from rest_framework import serializers

from base.common.constant import message
from base.common.constant.db_fields import CommonFields, OrderFields
from base.common.utils.exceptions import APIErr
from base.common.utils.serializer import ForeignKeyField
from base.order.models import Order
from base.table.models import Table
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

    class Meta:
        model = OrderBaseSlz.Meta.model
        fields = OrderBaseSlz.Meta.fields + (OrderFields.TABLE_ID,)

    def create(self, validated_data):
        table_id = validated_data.get(OrderFields.TABLE_ID, 0)
        table = Table.objects.filter(id=table_id).first()
        if table and not table.is_available:
            raise APIErr(message.NOT_AVAILABLE)
        return super().create(validated_data)


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
