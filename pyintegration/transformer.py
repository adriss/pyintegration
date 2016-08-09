#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyintegration.component import Component


class Transformer(Component):
    '''
    Message Transformers play a very important role in enabling the loose-coupling 
    of Message Producers and Message Consumers. Rather than requiring every 
    Message-producing component to know what type is expected by the next consumer, 
    Transformers can be added between those components. Generic transformers, 
    such as one that converts a String to an XML Document, are also highly reusable.
    '''
    def __init__(self, transform):
        '''
        transform must return a 'Message'
        '''
        Component.__init__(self)
        self.transform = transform
        self.point_to_component = []

    def point_to(self, component):
        self.point_to_component.insert(0, component)

    '''
    Transform a message.
    '''
    def receive(self, message):
        '''
        Receives a message and sends it to its criteria.
        '''
        transformed_message = self.transform(message)
        self.message(transformed_message)
            
    def message(self, message):
        '''
        Sends the message to a single consumer.
        '''
        self.send_to_ref(self.point_to_component[0].ref(), message)   