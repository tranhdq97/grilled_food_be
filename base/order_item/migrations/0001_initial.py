# Generated by Django 4.1.10 on 2023-08-21 15:31

import base.common.constant.db_table
import base.common.models.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("order", "0001_initial"),
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.IntegerField()),
                (
                    "created_by",
                    base.common.models.base.CurrentUserField(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="%(app_label)s_%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name=base.common.constant.db_table.DBTable["ITEM"],
                        to="item.item",
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name=base.common.constant.db_table.DBTable[
                            "ORDER_ITEM"
                        ],
                        to="order.order",
                    ),
                ),
                (
                    "updated_by",
                    base.common.models.base.CurrentUserField(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name="%(app_label)s_%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": base.common.constant.db_table.DBTable["ORDER_ITEM"],
            },
        ),
    ]
