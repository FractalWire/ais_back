"""Module used to manage aisreceiver service"""
from __future__ import annotations
from time import sleep
import io
import csv
# import shutil

from core.models import BaseInfos, copy_csv

from .endpoints import aishubapi
from .app_settings import POSTGRES_WINDOW
from . import aisbuffer

import logging
from logformat import StyleAdapter

logger = StyleAdapter(logging.getLogger(__name__))


run = True


def start() -> None:

    logger.info("==== Starting AIS service ====")

    # 1) init redis
    # init_redis()

    # 2) launch endpoint listeners
    aishubapi.start()

    sleep(10)  # give endpoints time to start for immediate update

    logger.info("aishubapi endpoints started")
    logger.info("==============================")

    # 3) every X minutes :
    #    - update database from AisBuffer
    #    - flush AisBuffer
    while run:
        update_db()
        # TODO: sleep time do not take into account update_db process time
        sleep(POSTGRES_WINDOW)


def stop() -> None:
    pass


def update_db() -> None:
    """Update the database using messages stored in buffer"""

    logger.debug("starting database update")

    csv.register_dialect('postgres', delimiter='|', escapechar='\\',
                         lineterminator='\n', quoting=csv.QUOTE_NONE,
                         quotechar='', strict=True)
    f = io.StringIO()
    writer = csv.DictWriter(f, BaseInfos._aismeta.sorted_fields_name,
                            dialect='postgres')
    batch_size = 10000
    total_messages = 0
    logger.debug('preparing csv file for COPY using message_generator')
    for data in aisbuffer.messages.generator(batch_size):
        # Message.objects.bulk_create(messages, ignore_conflicts=True)
        writer.writerows(data)
        total_messages += len(data)

    # f.seek(0)
    # with open('copy.csv', 'w') as file_copy:
    #     shutil.copyfileobj(f, file_copy)

    logger.debug('starting to COPY')
    f.seek(0)
    new_messages, new_shipinfos = copy_csv(f)
    f.close()

    # TODO: Maybe only useful in DEBUG mode...
    logger.debug("{} new messages added to the database, {} discarded",
                 new_messages, total_messages-new_messages)
    logger.debug("{} new ship infos added to the database, {} discarded",
                 new_shipinfos, total_messages-new_shipinfos)

    logger.info('database updated')
    logger.info("------------------------------")
