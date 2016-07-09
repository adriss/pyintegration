#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration import PyIntegration
from pyintegration.message import Message
from pyintegration.transformer import Transformer
import time

class CustomTransformer(Transformer):
    def transform(self, message):
        the_message = Message.from_message(message)
        headers = the_message.headers
        message_s = str(the_message.payload)
        message_s = 'was ' + message_s
        return Message(message_s, headers)

def test_channel_to_transformer():
    integration = PyIntegration()
    try:
        channel = integration.create_point_to_point_channel()
        transformer = integration.create_transformer_endpoint(CustomTransformer())
        channel.point_to(transformer)
        transformer.point_to(integration.error_channel())
        integration.start()
        channel.put(Message('hello'))
        channel.put(Message('bye'))
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()