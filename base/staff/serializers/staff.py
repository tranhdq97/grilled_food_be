from rest_framework import serializers

from base.common.constant.db_fields import UserFields, CommonFields
from base.master.serializers.base import MasterBaseSlz
from base.profile.serializers.profile import ProfileBaseSlz
from base.staff.models import Staff


class StaffBaseSlz(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            CommonFields.ID,
            UserFields.EMAIL,
        )


class StaffRetrieveSlz(StaffBaseSlz):
    type = MasterBaseSlz()
    profile = ProfileBaseSlz(required=False)

    class Meta:
        model = StaffBaseSlz.Meta.model
        fields = StaffBaseSlz.Meta.fields + (CommonFields.TYPE,) + (UserFields.PROFILE,)
