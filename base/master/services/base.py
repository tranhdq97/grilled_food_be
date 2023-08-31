from typing import Optional

from django.apps import apps
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from ...common.constant import message
from ...common.constant.app_label import ModelAppLabel
from ...common.constant.db_table import DBTable
from ...common.constant.service import Master
from ...common.utils.exceptions import APIErr
from ...master.serializers.base import MasterBaseSlz
from ...master.serializers.city import MasterCitySlz
from ...master.serializers.country import MasterCountrySlz
from ...master.serializers.district import MasterDistrictSlz


class MasterBaseService:
    def __init__(self, master_name):
        self.table_name, self.model_name, self.allowed_to_create = Master.unpack(
            master_name
        )
        self.model = apps.get_model(ModelAppLabel.MASTER, self.model_name)
        slz_switcher = {
            DBTable.MASTER_COUNTRY: MasterCountrySlz,
            DBTable.MASTER_DISTRICT: MasterDistrictSlz,
            DBTable.MASTER_CITY: MasterCitySlz,
        }
        self.slz = slz_switcher.get(self.table_name, MasterBaseSlz)

    def get_item_by_id(self, pk: int):
        return get_object_or_404(self.model, pk=pk)

    def list(self, parent_id: Optional[int] = None) -> list:
        qs_conditions = dict()
        if parent_id:
            if self.table_name == DBTable.MASTER_CITY:
                qs_conditions.update(country_id=parent_id)
            elif self.table_name == DBTable.MASTER_DISTRICT:
                qs_conditions.update(city_id=parent_id)

        return self.model.objects.filter(**qs_conditions)

    def create(self, data: dict):
        if not self.allowed_to_create:
            raise APIErr(message.NOT_ALLOWED_TO_CREATE)

        slz_instance = self.slz(data=data)
        slz_instance.is_valid(raise_exception=True)
        try:
            instance = self.model.objects.create(**slz_instance.validated_data)
        except IntegrityError:
            instance = self.model.objects.filter(**slz_instance.validated_data).first()
            instance.is_deleted = False
            instance.save()
        except Exception:
            raise APIErr(message.INVALID_INPUT)
        return self.slz(instance)

    def delete(self, pk: int):
        instance = self.get_item_by_id(pk)
        instance.is_deleted = True
        instance.save()
