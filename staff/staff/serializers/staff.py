from django.db import transaction
from rest_framework import serializers

from base.common.constant import message
from base.common.constant.constant import RegexPattern
from base.common.constant.db_fields import CommonFields, UserFields
from base.common.utils.exceptions import APIErr
from base.common.utils.serializer import ForeignKeyField
from base.common.utils.strings import check_regex
from base.master.models import MasterStaffType
from base.master.serializers.base import MasterBaseSlz
from base.staff.models.staff import Staff
from ...profile.serializers.profile import (
    ProfileRetrieveSlz,
    ProfileForUserListSlz,
    ProfileUpdateSlz,
    ProfileCreateSlz,
)


class StaffBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (CommonFields.ID, UserFields.EMAIL)


class StaffRetrieveSlz(StaffBaseSlz):
    type = MasterBaseSlz()
    profile = ProfileRetrieveSlz()

    class Meta:
        model = StaffBaseSlz.Meta.model
        fields = (
            StaffBaseSlz.Meta.fields
            + (UserFields.PROFILE,)
            + (
                CommonFields.TYPE,
                CommonFields.UPDATED_AT,
            )
        )


class StaffListSlz(StaffBaseSlz):
    type = MasterBaseSlz()
    profile = ProfileForUserListSlz()

    class Meta:
        model = StaffBaseSlz.Meta.model
        fields = StaffBaseSlz.Meta.fields + (UserFields.PROFILE,) + (CommonFields.TYPE,)


class StaffUpdateSlz(StaffBaseSlz):
    type_id = ForeignKeyField(MasterStaffType, write_only=True, required=False)
    type = MasterBaseSlz(read_only=True)
    profile = ProfileUpdateSlz(required=False)

    class Meta:
        model = StaffBaseSlz.Meta.model
        fields = (
            StaffBaseSlz.Meta.fields
            + (
                CommonFields.TYPE_ID,
                CommonFields.TYPE,
            )
            + (UserFields.PROFILE,)
        )
        extra_kwargs = {UserFields.EMAIL: {"read_only": True}}

    def update(self, instance, validated_data):
        with transaction.atomic():
            profile_data = validated_data.get(UserFields.PROFILE, {})
            type_id = validated_data.get(CommonFields.TYPE_ID)
            if profile_data:
                if instance.profile:
                    slz = ProfileUpdateSlz(instance=instance.profile, data=profile_data)
                else:
                    slz = ProfileCreateSlz(data=dict(profile_data))
                slz.is_valid(raise_exception=True)
                slz.save()
                if not instance.profile_id:
                    instance.profile_id = slz.data.get(CommonFields.ID)
            if type_id:
                instance.type_id = type_id
            instance.save()
            return instance


class StaffCreateSlz(StaffBaseSlz):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = StaffBaseSlz.Meta.model
        fields = StaffBaseSlz.Meta.fields + (
            UserFields.EMAIL,
            UserFields.PASSWORD,
        )

    def validate(self, attrs):
        email = attrs.get(UserFields.EMAIL)
        password = attrs.get(UserFields.PASSWORD)
        if not email:
            raise APIErr(message.MUST_HAVE_EMAIL)

        if self.Meta.model.objects.filter(email=email).exists():
            raise APIErr(message.ALREADY_EXISTS)

        if not check_regex(RegexPattern.PASSWORD, password):
            raise APIErr(message.PASSWORD_INAPPROPRIATE)

        if email == password:
            raise APIErr(message.PASSWORD_MUST_DIFFER_EMAIL)

        return attrs

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)
