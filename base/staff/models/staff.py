from django.db import models

from base.common.constant.app_label import ModelAppLabel
from base.common.constant.db_table import DBTable
from base.common.constant.master import MasterStaffTypeID
from base.common.models.base import CustomBaseUserModel
from base.master.models import MasterStaffType
from base.profile.models import Profile


class Staff(CustomBaseUserModel):
    is_admin = models.BooleanField(default=False)
    profile = models.OneToOneField(Profile, on_delete=models.RESTRICT, null=True, related_name=DBTable.STAFF)
    type = models.ForeignKey(
        MasterStaffType,
        on_delete=models.RESTRICT,
        default=MasterStaffTypeID.UNAPPROVED,
        related_name=DBTable.STAFF,
    )

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self) -> bool:
        return True

    @property
    def is_super_staff(self) -> bool:
        return bool(self.is_admin)

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.type_id = MasterStaffTypeID.SUPER_STAFF
        super(Staff, self).save(*args, **kwargs)

    class Meta:
        db_table = DBTable.STAFF
        app_label = ModelAppLabel.STAFF
