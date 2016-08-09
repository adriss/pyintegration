#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging

from pyintegration import PyIntegration
from pyintegration.channel import PointToPointThreadingChannel
from pyintegration.message import Message
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def test_1_message_no_pipe():
    channel1 = PointToPointThreadingChannel()
    assert 0 == channel1.size()
    payload = 'some payload'
    message = Message(payload)
    channel1.put(message)
    assert 1 == channel1.size()

def test_pipe_2_channels_no_message():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    try:
        channel2.consume(channel1)
    finally:
        PyIntegration.stop_all()

def test_2_channels_message_no_pipe():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    assert 0 == channel1.size()
    assert 0 == channel2.size()
    channel1.put(Message('hello'))
    assert 1 == channel1.size()
    assert 0 == channel2.size()

def test_1_channel_consumes_from_other():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    try:
        channel1.put(Message('hello'))
        assert 1 == channel1.size()
        assert 0 == channel2.size()
        channel2.consume(channel1)
        time.sleep(1)
        assert 0 == channel1.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()

def test_1_channel_produces_to_other():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    try:
        channel1.put(Message('hello'))
        assert 1 == channel1.size()
        assert 0 == channel2.size()
        channel1.produce(channel2)
        time.sleep(1)
        assert 0 == channel1.size()
        assert 1 == channel2.size()
    finally:
        PyIntegration.stop_all()

def test_3_channels_message():
    channel1 = PointToPointThreadingChannel()
    channel2 = PointToPointThreadingChannel()
    channel3 = PointToPointThreadingChannel()
    try:
        channel1.put(Message('hello'))
        channel2.put(Message('bye'))
        channel2.consume(channel1)
        channel3.consume(channel2)
        time.sleep(1)
        assert 0 == channel1.size()
        assert 0 == channel2.size()
        assert 2 == channel3.size()
    finally:
        PyIntegration.stop_all()