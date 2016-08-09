#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from pyintegration import PyIntegration
from pyintegration.message import Message

test_string = 'was '

def transform(message):
    headers = message.headers
    message_s = str(message.payload)
    message_s = test_string + message_s
    return Message(message_s, headers)

def test_channel_to_transformer(capsys):
    integration = PyIntegration()
    try:
        channel = integration.create_point_to_point_channel()
        transformer = integration.create_transformer(transform)
        channel.point_to(transformer)
        transformer.point_to(integration.error_channel())
        integration.start()
        channel.put(Message('hello'))
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()
        out, err = capsys.readouterr()
        assert test_string in err
        # assert out == ''