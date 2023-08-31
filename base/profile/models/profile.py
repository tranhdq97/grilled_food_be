from django.db import models

from base.address.models import Address
from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.models.base import DateTimeModel
from base.master.models import MasterSex


class Profile(DateTimeModel):
    phone_number = models.CharField(max_length=12, null=True, unique=True)
    first_name = models.CharField(max_length=32, null=True)
    last_name = models.CharField(max_length=32, null=True)
    dob = models.DateField(null=True)
    citizen_number = models.CharField(max_length=12, null=False, unique=True)
    address = models.ForeignKey(
        Address, on_delete=models.RESTRICT, null=True, related_name=DBTable.PROFILE
    )
    sex = models.ForeignKey(
        MasterSex, on_delete=models.RESTRICT, null=True, related_name=DBTable.PROFILE
    )

    class Meta:
        db_table = DBTable.PROFILE
        app_label = ModelAppLabel.PROFILE
