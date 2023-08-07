from rest_framework import serializers

from base.address.models import Address
from base.common.constant.db_fields import CommonFields, AddressFields
from base.common.utils.serializer import ForeignKeyField
from base.master.models import MasterDistrict
from base.master.serializers.district import MasterDistrictSlz


class AddressBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (CommonFields.ID, AddressFields.STREET)


class AddressCreateSlz(AddressBaseSlz):
    district_id = ForeignKeyField(MasterDistrict)

    class Meta:
        model = AddressBaseSlz.Meta.model
        fields = AddressBaseSlz.Meta.fields + (AddressFields.DISTRICT_ID,)


class AddressRetrieveSlz(AddressBaseSlz):
    district = MasterDistrictSlz()

    class Meta:
        model = AddressBaseSlz.Meta.model
        fields = AddressBaseSlz.Meta.fields + (AddressFields.DISTRICT,)


class AddressListSlz(AddressRetrieveSlz):
    class Meta:
        model = AddressBaseSlz.Meta.model
        fields = AddressBaseSlz.Meta.fields + (AddressFields.DISTRICT,)


class AddressUpdateSlz(AddressBaseSlz):
    class Meta:
        model = AddressBaseSlz.Meta.model
        fields = AddressBaseSlz.Meta.fields
