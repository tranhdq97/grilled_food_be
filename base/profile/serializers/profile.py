from rest_framework import serializers

from base.common.constant.db_fields import CommonFields, ProfileFields
from base.master.serializers.base import MasterBaseSlz
from base.profile.models import Profile


class ProfileBaseSlz(serializers.ModelSerializer):
    sex = MasterBaseSlz()

    class Meta:
        model = Profile
        fields = (
            CommonFields.ID,
            ProfileFields.FIRST_NAME,
            ProfileFields.LAST_NAME,
            ProfileFields.PHONE_NUMBER,
            ProfileFields.SEX,
        )
