#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid


class MessageHeaders(dict):
    def __init__(self, *args, **kw):
        super(MessageHeaders, self).__init__(*args, **kw)

class Message(object):
    '''
    A Message is a generic wrapper for any Python object combined with metadata used by 
    the framework while handling that object. It consists of a payload and headers. For 
    example, when creating a Message from a received File, the file name may be stored in 
    a header to be accessed by downstream components. Likewise, if a Message’s content is 
    ultimately going to be sent by an outbound Mail adapter, the various properties (to, 
    from, cc, subject, etc.) may be configured as Message header values by an upstream 
    component. Developers can also store any arbitrary key-value pairs in the headers.
    '''
    def __init__(self, payload, headers=MessageHeaders()):
        self.pl = payload
        self.hs = headers
        self.hs['UUID'] = str(uuid.uuid4())
      
    def payload(self):
        '''
        The payload can be of any type and the headers hold commonly required information 
        such as id, timestamp, correlation id, and return address. Headers are also used 
        for passing values to and from connected transports.
        '''
        return self.pl
    
    def headers(self):
        '''
        Headers are also used for passing values to and from connected transports.
        '''
        return self.hs
    
    def __str__(self):
        return '[headers:' + str(self.hs) + ', payload:' + str(self.pl) + ']'