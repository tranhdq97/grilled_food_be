from rest_framework import serializers

from base.common.constant.db_fields import CommonFields, TableFields
from base.common.utils.serializer import ForeignKeyField
from base.staff.models import Staff
from base.staff.serializers.staff import StaffRetrieveSlz
from base.table.models import Table


class TableBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = (
            CommonFields.ID,
            CommonFields.NAME,
            TableFields.IS_AVAILABLE,
        )


class TableCreateSlz(TableBaseSlz):
    class Meta:
        model = TableBaseSlz.Meta.model
        fields = TableBaseSlz.Meta.fields
        extra_kwargs = {TableFields.IS_AVAILABLE: {"read_only": True}}


class TableUpdateSlz(TableBaseSlz):
    class Meta:
        model = TableBaseSlz.Meta.model
        fields = TableBaseSlz.Meta.fields
        extra_kwargs = {CommonFields.NAME: {"read_only": True}}


class TableUpdateStaffInOutSlz(TableBaseSlz):
    in_table_staff_id = ForeignKeyField(model=Staff, required=False, read_only=True)

    class Meta:
        model = TableBaseSlz.Meta.model
        fields = TableBaseSlz.Meta.fields + (TableFields.IN_TABLE_STAFF_ID,)
        extra_kwargs = {
            CommonFields.NAME: {"read_only": True},
            TableFields.IS_AVAILABLE: {"read_only": True},
        }


class TableRetrieveSlz(TableBaseSlz):
    in_table_staff = StaffRetrieveSlz()

    class Meta:
        model = TableBaseSlz.Meta.model
        fields = TableBaseSlz.Meta.fields + (TableFields.IN_TABLE_STAFF,)


class TableListSlz(TableBaseSlz):
    in_table_staff = StaffRetrieveSlz()

    class Meta:
        model = TableBaseSlz.Meta.model
        fields = TableBaseSlz.Meta.fields + (TableFields.IN_TABLE_STAFF,)
