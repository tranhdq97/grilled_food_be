import logging
import pathlib

from django.core import serializers
from django.core.management.base import BaseCommand
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @staticmethod
    def __insert_data(folder: str):
        for file in pathlib.Path(folder).rglob("*.json"):
            logger.info(f"File: {file}")
            if not file.is_file():
                continue

            with file.open() as f:
                data = f.read()

            for item in serializers.deserialize("json", data):
                try:
                    item.save()
                except IntegrityError as err:
                    logger.error(err)

    def handle(self, *args, **options):
        logger.info("Master data initializing called.")
        try:
            self.__insert_data(folder="base/master/assets")
            logger.info("Master data initializing success.")
        except Exception as e:
            logger.error("Master data initializing failed", exc_info=e)
