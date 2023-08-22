from rest_framework import serializers

from base.address.models import Address
from base.common.constant.db_fields import CommonFields, ProfileFields
from base.common.utils.serializer import ForeignKeyField
from base.master.models import MasterSex
from base.master.serializers.base import MasterBaseSlz
from base.profile.models import Profile
from staff.address.serializers.address import AddressRetrieveSlz, AddressListSlz


class ProfileBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            CommonFields.ID,
            ProfileFields.PHONE_NUMBER,
            ProfileFields.LAST_NAME,
            ProfileFields.FIRST_NAME,
        )


class ProfileCreateSlz(ProfileBaseSlz):
    address_id = ForeignKeyField(Address, required=False, write_only=True)
    sex_id = ForeignKeyField(MasterSex, required=False, write_only=True)
    address = AddressRetrieveSlz(read_only=True)
    sex = MasterBaseSlz(read_only=True)

    class Meta:
        model = ProfileBaseSlz.Meta.model
        fields = ProfileBaseSlz.Meta.fields + (
            ProfileFields.DOB,
            ProfileFields.ADDRESS_ID,
            ProfileFields.SEX_ID,
            ProfileFields.ADDRESS,
            ProfileFields.SEX,
        )


class ProfileRetrieveSlz(ProfileBaseSlz):
    address = AddressRetrieveSlz()
    sex = MasterBaseSlz()

    class Meta:
        model = ProfileBaseSlz.Meta.model
        fields = ProfileBaseSlz.Meta.fields + (
            ProfileFields.DOB,
            ProfileFields.ADDRESS,
            ProfileFields.SEX,
        )


class ProfileForUserListSlz(ProfileBaseSlz):
    address = AddressListSlz()
    sex = MasterBaseSlz()

    class Meta:
        model = ProfileBaseSlz.Meta.model
        fields = ProfileBaseSlz.Meta.fields + (
            ProfileFields.DOB,
            ProfileFields.ADDRESS,
            ProfileFields.SEX,
        )


class ProfileUpdateSlz(ProfileCreateSlz):
    class Meta:
        model = ProfileCreateSlz.Meta.model
        fields = ProfileCreateSlz.Meta.fields
