"""Module used to manage aisreceiver service"""
from __future__ import annotations
from typing import List
from time import sleep

from core.models import Message
from .endpoints import aishubapi
from .aismessage import Infos, Position, default_infos, infos_keys
from .buffer import position_buffer, infos_buffer, buffer_lock

import logging
from logformat import StyleAdapter

logger = StyleAdapter(logging.getLogger(__name__))

# Update interval to store the latest position received
# TODO: put that in a config file maybe
MESSAGE_UPDATE_WINDOW = 5*60  # in seconds


run = True


def start() -> None:

    logger.info("==== Starting AIS service ====")
    # logger.debug("Just a test")
    # 1) init infos_buffer
    with buffer_lock:
        init_infos_buffer()

    logger.info("infos_buffer initialized")

    # 2) launch endpoint listeners
    aishubapi.start()
    logger.info("aishubapi endpoints started")

    sleep(10)  # give endpoints time to start for immediate update

    # 3) every X minutes :
    #    - update database from position_buffer and infos_buffer
    #    - flush positions_buffer

    while run:

        logger.debug("starting database update")
        with buffer_lock:
            logger.debug("buffer_lock acquired")
            messages_before = Message.objects.count()
            messages = make_bulk_messages()
            messages_len = len(messages)
            Message.objects.bulk_create(messages, ignore_conflicts=True)
            messages_after = Message.objects.count()

            position_buffer.clear()
            logger.debug("position_buffer cleared")

        # TODO: Maybe only useful in DEBUG mode...
        new_messages = messages_after-messages_before
        logger.info("{} new messages added to the database, {} discarded",
                    new_messages, messages_len-new_messages)

        sleep(MESSAGE_UPDATE_WINDOW)


def stop() -> None:
    pass


def init_infos_buffer() -> None:
    """Initialises infos_buffer with existing corresponding Message fields from 
    the database"""

    last_infos = (Message.objects.distinct('mmsi')
                  .order_by('mmsi', '-time')
                  .values(*infos_keys))
    infos_buffer.clear()
    for infos in last_infos:
        infos_buffer[infos['mmsi']] = Infos(**infos)


def make_bulk_messages() -> List[Message]:
    """Creates a message list for following batch processing to the database
    based on infos_dict and positions_dict"""

    messages = []

    for mmsi, position in position_buffer.items():
        infos = mmsi in infos_buffer and infos_buffer[mmsi] or default_infos
        message = Message(
            mmsi=mmsi,
            time=position.time,
            point=position.point,
            cog=position.cog,
            sog=position.sog,
            heading=position.heading,
            pac=position.pac,
            rot=position.rot,
            navstat=position.navstat,

            imo=infos.imo,
            callsign=infos.callsign,
            name=infos.name,
            ship_type=infos.ship_type,
            dim_bow=infos.dim_bow,
            dim_stern=infos.dim_stern,
            dim_port=infos.dim_port,
            dim_starboard=infos.dim_starboard,
            eta=infos.eta,
            draught=infos.draught,
            destination=infos.destination
        )
        messages.append(message)

    return messages
