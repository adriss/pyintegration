#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
import sys

from pyintegration import PyIntegration
from pyintegration.message import Message
from pyintegration.channel import PointToPointThreadingChannel
from pyintegration.transformer import Transformer
logger = logging.getLogger('pyintegration')

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

test_string = 'was '

def transform(message):
    logger.debug('message:' + str(message))
    headers = message.headers()
    logger.debug('headers:' + str(headers))
    message_s = str(message.payload())
    message_s = test_string + message_s
    return Message(message_s, headers)

def test_transformer_no_inout():
    logger.debug('running test_transformer_no_inout')
    logger.debug('creating transformer')
    Transformer(transform)

def test_transformer_no_out():
    try:
        logger.debug('running test_transformer_no_inout')
        logger.debug('creating transformer')
        transformer = Transformer(transform)
        logger.debug('creating channel1')
        channel1 = PointToPointThreadingChannel()
        transformer.input_channel(channel1)
        channel1.put(Message('hello'))
        time.sleep(1)  # wait for flow to drain
        assert 1 == channel1.size()
    finally:
        PyIntegration.stop_all()

def test_transformer():
    try:
        logger.debug('running test_transformer_no_inout')
        logger.debug('creating transformer')
        transformer = Transformer(transform)
        logger.debug('creating channel1')
        channel1 = PointToPointThreadingChannel('channel1')
        transformer.input_channel(channel1)
        logger.debug('creating channel2')
        channel2 = PointToPointThreadingChannel('channel2')
        transformer.output_channel(channel2)
        channel1.put(Message('hello'))
        time.sleep(1)  # wait for flow to drain
        assert 0 == channel1.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()
