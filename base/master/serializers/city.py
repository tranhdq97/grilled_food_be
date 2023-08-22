from rest_framework import serializers

from base.common.constant.db_fields import CommonFields, MasterFields, MasterCityFields
from base.master.models.district import MasterCity
from base.master.serializers.country import MasterCountrySlz


class MasterCitySlz(serializers.ModelSerializer):
    country = MasterCountrySlz()

    class Meta:
        model = MasterCity
        fields = (CommonFields.ID, MasterFields.NAME, MasterCityFields.COUNTRY)
