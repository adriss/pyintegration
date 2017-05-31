#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging

from pyintegration import PyIntegration
from pyintegration.channel import PointToPointThreadingChannel
from pyintegration.message import Message
import sys
logger = logging.getLogger('pyintegration')

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def test_1_message_no_pipe():
    logger.debug('running test_1_message_no_pipe')
    channel1 = PointToPointThreadingChannel('channel1')
    assert 0 == channel1.size()
    payload = 'some payload'
    message = Message(payload)
    channel1.put(message)
    assert 1 == channel1.size()
    time.sleep(1)
    
def test_pipe_2_channels_no_message():
    logger.debug('running test_pipe_2_channels_no_message')
    logger.debug('creating channel1')
    channel1 = PointToPointThreadingChannel('channel1')
    logger.debug('creating channel2')
    channel2 = PointToPointThreadingChannel('channel1')
    try:
        logger.debug('start consuming channel1 from channel2')
        channel2.consume(channel1)
        time.sleep(.005)
    finally:
        PyIntegration.stop_all()

def test_2_channels_message_no_consumption():
    logger.debug('running test_pipe_2_channels_no_message')
    logger.debug('creating channel1')
    channel1 = PointToPointThreadingChannel()
    logger.debug('creating channel2')
    channel2 = PointToPointThreadingChannel()
    assert 0 == channel1.size()
    assert 0 == channel2.size()
    logger.debug('putting message in channel1')
    channel1.put(Message('test_2_channels_message_no_pipe'))
    assert 1 == channel1.size()
    assert 0 == channel2.size()

def test_1_channel_consumes_from_other():
    logger.debug('running test_pipe_2_channels_no_message')
    logger.debug('creating channel1')
    channel1 = PointToPointThreadingChannel('channel1')
    logger.debug('creating channel2')
    channel2 = PointToPointThreadingChannel('channel2')
    try:
        logger.debug('putting message in channel1')
        channel1.put(Message('test_1_channel_consumes_from_other'))
        assert 1 == channel1.size()
        assert 0 == channel2.size()
        logger.debug('start consuming channel1 from channel2')
        channel2.consume(channel1)
        logger.debug('sleeping...')
        time.sleep(.005)
        logger.debug('waking...')
        assert 0 == channel1.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()

def test_1_channel_produces_to_other():
    logger.debug('running test_1_channel_produces_to_other')
    logger.debug('creating channel1')
    channel1 = PointToPointThreadingChannel('channel1')
    logger.debug('creating channel2')
    channel2 = PointToPointThreadingChannel('channel2')
    try:
        channel1.put(Message('test_1_channel_produces_to_other'))
        assert 1 == channel1.size()
        assert 0 == channel2.size()
        channel1.produce(channel2)
        time.sleep(.005)
        assert 0 == channel1.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()

def test_3_channels_message():
    channel1 = PointToPointThreadingChannel('channel1')
    channel2 = PointToPointThreadingChannel('channel2')
    channel3 = PointToPointThreadingChannel('channel3')
    try:
        channel1.put(Message('test_3_channels_message-1'))
        channel2.put(Message('test_3_channels_message-2'))
        channel2.consume(channel1)
        channel3.consume(channel2)
        time.sleep(1)
        assert 0 == channel1.size()
        assert 0 == channel2.size()
        assert 2 == channel3.size()
    finally:
        PyIntegration.stop_all()