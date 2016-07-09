#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration import PyIntegration
from pyintegration.message import Message
import time
from pyintegration.filter import Filter

class BlockFilter(Filter):
    def accept(self, message):
        message_s = str(Message.from_message(message))
        if 'block' in message_s:
            return False
        else:
            return True

def test_channel_to_filter():
    integration = PyIntegration()
    try:
        channel = integration.create_point_to_point_channel()
        filter_endpoint = integration.create_filter_endpoint(BlockFilter())
        channel.point_to(filter_endpoint)
        filter_endpoint.point_to(integration.error_channel())
        integration.start()
        channel.put(Message('block this message'))
        channel.put(Message('another message'))
        time.sleep(1) # wait for flow to drain
    finally:
        integration.stop()