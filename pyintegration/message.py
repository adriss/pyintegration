#!/usr/bin/env python
# -*- coding: utf-8 -*-
class MessageHeaders(dict):
    def __init__(self, *args, **kw):
        super(MessageHeaders, self).__init__(*args, **kw)

class Message(object):
    
    def __init__(self, payload, headers=MessageHeaders()):
        self.payload = payload
        self.headers = headers
    
    @staticmethod
    def MESSAGE_KEY():
        return 'message'

    @staticmethod
    def to_message(message):
        if isinstance(message, dict) and Message.MESSAGE_KEY() in message:
            return message
        else:
            return {Message.MESSAGE_KEY() : message}
            
    @staticmethod
    def from_message(message):
        return message[Message.MESSAGE_KEY()]
        
    def payload(self):
        return self.payload
    
    def headers(self):
        return self.headers
    
    def __str__(self):
        return '[headers:' + str(self.headers) + ', payload:' + str(self.payload) + ']'