#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pyintegration.component import Component
from pyintegration.message import Message


class Channel(Component):
    '''
    A Message Channel represents the "pipe" of a pipes-and-filters architecture. 
    Producers send Messages to a channel, and consumers receive Messages from a channel. 
    The Message Channel therefore decouples the messaging components, and also provides a convenient 
    point for interception and monitoring of Messages.
    '''
    def __init__(self):
        Component.__init__(self)
        
    def point_to(self, component):
        raise Exception('Not Implemented')
    
    def receive(self, message):
        raise Exception('Not Implemented')
    
    def put(self, message):
        raise Exception('Not Implemented')

class PointToPointChannel(Channel):
    '''
    With a Point-to-Point channel, at most one consumer can receive each Message sent to the channel.
    '''
    def __init__(self):
        Component.__init__(self)
        self.point_to_component = []
        
    def point_to(self, consumer):
        '''
        Sets the consumer of this point-to-point channel.
        '''
        self.point_to_component.insert(0, consumer)
    
    def receive(self, message):
        '''
        Receives a message and sends it to its consumer.
        '''
        return self.message(message)
    
    def put(self, message):
        '''
        Sends a message to its consumer.
        '''
        return self.message(message)
    
    def message(self, message):
        '''
        Sends the message to a single consumer.
        '''
        self.send_to_ref(self.point_to_component[0].ref(), Message.to_message(message))

class ErrorChannel(Channel):
    def __init__(self):
        Channel.__init__(self)

    def receive(self, message):
        '''
        Receives a message and prints it to STDERR.
        '''
        sys.stderr.write('[ErrorChannel]' + str(Message.from_message(message)))
        return message