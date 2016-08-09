#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging

from pyintegration import PyIntegration
from pyintegration.message import Message
from pyintegration.channel import PointToPointThreadingChannel
from pyintegration.filter import Filter
import sys

logger = logging.getLogger('pyintegration')
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def accept(message):
    message_s = message.payload()
    if 'block' in message_s:
        return False
    else:
        return True

def test_block_message():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    the_filter = Filter(accept)
    try:
        channel1.put(Message('block this message'))
        assert 1 == channel1.size()
        assert 0 == the_filter.size()
        assert 0 == channel2.size()
        the_filter.consume(channel1)
        time.sleep(1) # wait for flow to drain
        assert 0 == channel1.size()
        assert 0 == the_filter.size()
        assert 0 == channel2.size()
        the_filter.produce(channel2)
        time.sleep(1) # wait for flow to drain
        assert 0 == channel1.size()
        assert 0 == the_filter.size()
        assert 0 == channel2.size()
    finally:
        PyIntegration.stop_all()

def test_accept_message():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    the_filter = Filter(accept)
    try:
        channel1.put(Message('accept this message'))
        assert 1 == channel1.size()
        assert 0 == the_filter.size()
        assert 0 == channel2.size()
        the_filter.consume(channel1)
        time.sleep(1) # wait for flow to drain
        assert 0 == channel1.size()
        assert 1 == the_filter.size()
        assert 0 == channel2.size()
        the_filter.produce(channel2)
        time.sleep(1) # wait for flow to drain
        assert 0 == channel1.size()
        assert 0 == the_filter.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()