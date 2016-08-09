#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration.message import Message


def test_payload(capsys):
    payload = 'hello'
    message = Message(payload)
    assert payload == message.payload()

def test_default_headers(capsys):
    payload = 'hello'
    message = Message(payload)
    assert 0 == len(message.headers())

def test_headers(capsys):
    payload = 'hello'
    headers = {'Name': 'Zara'};
    message = Message(payload, headers)
    assert headers == message.headers()