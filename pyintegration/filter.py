#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyintegration.component import Component
from pyintegration.message import Message

class FilterEndpoint(Component):
    '''
    Filters are used to decide whether a Message should be passed along or 
    dropped based on some 'criteria' such as a Message Header value or even content 
    within the Message itself. Therefore, a Message Filter is similar to a router, 
    except that for each Message received from the filter's input channel, 
    that same Message may or may not be sent to the filter's output channel. 
    Unlike the router, it makes no decision regarding which Message Channel to 
    send to but only decides whether to send.
    '''
    def __init__(self, selector):
        Component.__init__(self)
        self.selector = selector
        self.point_to_component = []

    def point_to(self, component):
        self.point_to_component.insert(0, component)

    '''
    Filters a message.
    '''
    def receive(self, message):
        '''
        Receives a message and sends it to its consumer.
        '''
        if self.selector.accept(message):
            self.message(message)
        # silent drop message
            
    def message(self, message):
        '''
        Sends the message to a single consumer.
        '''
        self.send_to_ref(self.point_to_component[0].ref(), Message.to_message(message))   

class Filter(object):
    '''
    Returns true if the message should be accepted.
    '''
    def accept(self, message):
        raise Exception('Not Implemented')