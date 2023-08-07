from abc import abstractmethod

from crum import get_current_user
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import ForeignKey, Manager, QuerySet

from base.common.models.managers import CustomUserManager


class AppQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class AppManager(Manager):
    def get_queryset(self):
        return AppQuerySet(self.model, using=self._db).exclude(is_deleted=True)


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = AppManager()

    def delete(self):
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True


class CurrentUserField(ForeignKey):
    def __init__(self, to, **kwargs):
        self.auto_current = kwargs.pop("auto_current", False)
        self.auto_current_add = kwargs.pop("auto_current_add", False)
        super().__init__(to, **kwargs)

    def pre_save(self, model_instance, add):
        if self.auto_current or (self.auto_current_add and add):
            current_user = get_current_user()
            if current_user and current_user.is_authenticated:
                user_id = current_user.id
                setattr(model_instance, self.attname, user_id)
                return user_id

        return super().pre_save(model_instance, add)


class Creator(models.Model):
    created_by = CurrentUserField(
        to="staff.Staff",
        auto_current_add=True,
        null=True,
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_created_by",
    )

    class Meta:
        abstract = True


class Editor(models.Model):
    updated_by = CurrentUserField(
        to="staff.Staff",
        auto_current=True,
        null=True,
        on_delete=models.RESTRICT,
        related_name="%(app_label)s_%(class)s_updated_by",
    )

    class Meta:
        abstract = True


class DateTimeModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        abstract = True


class CustomBaseUserModel(AbstractBaseUser, DateTimeModel):
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_leave = models.BooleanField(default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @abstractmethod
    def is_staff(self):
        pass

    def __str__(self):
        return f"{self.email}"

    class Meta:
        abstract = True


class MasterBaseModel(BaseModel):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
