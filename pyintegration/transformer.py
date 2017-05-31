#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration.component import ThreadingComponent
import logging

logger = logging.getLogger('pyintegration')

class Transformer(ThreadingComponent):

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
        super(Transformer, self).__init__()
        self.transform = transform
        self.the_input_channel = None
        self.the_output_channel = None

    def input_channel(self, the_input_channel):
        self.the_input_channel = the_input_channel

    def output_channel(self, the_output_channel):
        self.the_output_channel = the_output_channel
        self.consume(self.the_input_channel)
        self.the_output_channel.consume(self)

    def produce_on_receive(self, message, queue):
        the_message = super(Transformer, self).produce_on_receive(message, queue)
        if the_message is not None:
            the_message = self.transform(the_message)
        return the_message