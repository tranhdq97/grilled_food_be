from rest_framework import serializers

from base.common.constant.db_fields import (
    CommonFields,
    MasterFields,
    MasterCountryFields,
)
from base.master.models import MasterCountry


class MasterCountrySlz(serializers.ModelSerializer):
    class Meta:
        model = MasterCountry
        fields = (CommonFields.ID, MasterFields.NAME, MasterCountryFields.CODE)
