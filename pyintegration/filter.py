#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyintegration.component import ThreadingComponent
from Queue import Queue
import logging

logger = logging.getLogger('pyintegration')

class FilterQueue(Queue):
    def __init__(self, accept):
        Queue.__init__(self)
        self.accept = accept

    def put(self, message, block=True, timeout=None):
        '''
        Receives a message and sends it to its consumer.
        '''
        if self.accept(message):
            logger.info('%s producing message:%s', self, message)
            Queue.put(self, message, block=block, timeout=timeout)

class Filter(ThreadingComponent):
    '''
    Filters are used to decide whether a Message should be passed along or 
    dropped based on some 'accept' criteria such as a Message Header value 
    or even content within the Message itself. Therefore, a Message Filter 
    is similar to a router, except that for each Message received from the 
    filter's input channel, that same Message may or may not be sent to the 
    filter's output channel. Unlike the router, it makes no decision regarding 
    which Message Channel to send to but only decides whether to send.
    '''
    def __init__(self, accept):
        super(Filter, self).__init__(FilterQueue(accept))
        self.accept = accept