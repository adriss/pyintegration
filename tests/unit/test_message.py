#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration.message import Message


def test_payload(capsys):
    payload = 'hello'
    message = Message(payload)
    assert payload == message.payload()