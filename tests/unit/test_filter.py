#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from pyintegration import PyIntegration
from pyintegration.message import Message


def accept(message):
    message_s = str(Message.from_message(message))
    if 'block' in message_s:
        return False
    else:
        return True

def test_block_message(capsys):
    integration = PyIntegration()
    try:
        channel = integration.create_point_to_point_channel()
        the_filter = integration.create_filter(accept)
        channel.point_to(the_filter)
        the_filter.point_to(integration.error_channel())
        integration.start()
        channel.put(Message('block this message'))
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()
        out, err = capsys.readouterr()
        assert err == ''
        assert out == ''
        
def test_accept_message(capsys):
    integration = PyIntegration()
    the_message = 'accept this message'
    try:
        channel = integration.create_point_to_point_channel()
        the_filter = integration.create_filter(accept)
        channel.point_to(the_filter)
        the_filter.point_to(integration.error_channel())
        integration.start()
        channel.put(Message(the_message))
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()
        out, err = capsys.readouterr()
        assert the_message in err
        assert out == ''
