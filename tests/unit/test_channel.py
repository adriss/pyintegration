#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration import PyIntegration
from pyintegration.message import Message


def test_channel_to_error_channel():
    integration = PyIntegration()
    try:
        channel = integration.create_point_to_point_channel()
        errorChannel = integration.create_error_channel()
        channel.point_to(errorChannel)
        integration.start()
        message = Message('Two Channels')
        channel.put(message)
    finally:
        integration.stop()

def test_channel_to_channel_to_error_channel():
    integration = PyIntegration()
    try:
        channel1 = integration.create_point_to_point_channel()
        channel2 = integration.create_point_to_point_channel()
        channel1.point_to(channel2)
        errorChannel = integration.create_error_channel()
        channel2.point_to(errorChannel)
        integration.start()
        message = Message('Three Channels')
        channel1.put(message)
    finally:
        integration.stop()