#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from pyintegration import PyIntegration
from pyintegration.message import Message


def test_channel_to_error_channel(capsys):
    integration = PyIntegration()
    the_message = 'Two Channels'
    try:
        channel = integration.create_point_to_point_channel()
        channel.point_to(integration.error_channel())
        integration.start()
        message = Message(the_message)
        channel.put(message)
    finally:
        integration.stop()
        out, err = capsys.readouterr()
        assert the_message in err
        assert out == ''

def test_channel_to_channel_to_error_channel(capsys):
    integration = PyIntegration()
    the_message = 'Three Channels'
    try:
        channel1 = integration.create_point_to_point_channel()
        channel2 = integration.create_point_to_point_channel()
        channel1.point_to(channel2)
        channel2.point_to(integration.error_channel())
        integration.start()
        message = Message(the_message)
        channel1.put(message)
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()
        out, err = capsys.readouterr()
        assert the_message in err
        assert out == ''