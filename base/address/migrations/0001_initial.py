# Generated by Django 4.1.10 on 2023-08-07 08:33

import base.common.constant.db_table
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        (base.common.constant.app_label.ModelAppLabel["MASTER"], "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("street", models.CharField(max_length=255, null=True)),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        related_name=base.common.constant.db_table.DBTable[
                            "MASTER_DISTRICT"
                        ],
                        to="master.masterdistrict",
                    ),
                ),
            ],
            options={
                "db_table": base.common.constant.db_table.DBTable["ADDRESS"],
            },
        ),
    ]
