from rest_framework import serializers

from base.common.constant.db_fields import (
    CommonFields,
    MasterDistrictFields,
    MasterFields,
)
from base.master.models.district import MasterDistrict
from base.master.serializers.city import MasterCitySlz


class MasterDistrictSlz(serializers.ModelSerializer):
    city = MasterCitySlz()

    class Meta:
        model = MasterDistrict
        fields = (
            CommonFields.ID,
            MasterFields.NAME,
            MasterDistrictFields.CITY,
            MasterDistrictFields.ZIP_CODE,
        )
