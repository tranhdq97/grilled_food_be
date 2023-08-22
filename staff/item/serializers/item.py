from rest_framework import serializers

from base.common.constant.db_fields import CommonFields, ItemFields
from base.common.utils.serializer import ForeignKeyField
from base.item.models import Item
from base.master.models import MasterItemType
from base.master.serializers.base import MasterBaseSlz


class ItemBaseSlz(serializers.ModelSerializer):
    num_ordered = serializers.IntegerField(read_only=True)

    class Meta:
        model = Item
        fields = (
            CommonFields.ID,
            CommonFields.NAME,
            ItemFields.PRICE,
        )


class ItemCreateSlz(ItemBaseSlz):
    type_id = ForeignKeyField(model=MasterItemType, write_only=True)
    type = MasterBaseSlz(read_only=True)

    class Meta:
        model = ItemBaseSlz.Meta.model
        fields = ItemBaseSlz.Meta.fields + (
            CommonFields.TYPE,
            CommonFields.TYPE_ID,
            CommonFields.TYPE_ID,
        )


class ItemUpdateSlz(ItemBaseSlz):
    type_id = ForeignKeyField(model=MasterItemType, required=False, write_only=True)
    type = MasterBaseSlz(read_only=True)

    class Meta:
        model = ItemBaseSlz.Meta.model
        fields = ItemBaseSlz.Meta.fields + (
            CommonFields.TYPE,
            CommonFields.TYPE_ID,
        )
        extra_kwargs = {
            CommonFields.NAME: {"required": False},
            ItemFields.PRICE: {"required": False},
        }


class ItemRetrieveSlz(ItemBaseSlz):
    type = MasterBaseSlz()

    class Meta:
        model = ItemBaseSlz.Meta.model
        fields = ItemBaseSlz.Meta.fields + (CommonFields.TYPE,)


class ItemListSlz(ItemBaseSlz):
    type = MasterBaseSlz()

    class Meta:
        model = ItemBaseSlz.Meta.model
        fields = ItemBaseSlz.Meta.fields + (CommonFields.TYPE,)
