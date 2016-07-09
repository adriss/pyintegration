#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pyintegration.channel import ErrorChannel, PointToPointChannel
from pyintegration.filter import Filter, FilterEndpoint


class PyIntegration(object):
    '''
    Python Enterprise Integration Framework.
    '''
    def __init__(self):
        self.components = list()
        self.the_error_channel = ErrorChannel()
        self.components.append(self.the_error_channel)
        
    def create_point_to_point_channel(self):
        '''
        Creates a Point-to-Point Channel.
        '''
        channel = PointToPointChannel()
        self.components.append(channel)
        return channel

    def error_channel(self):
        '''
        Returns the Error Channel
        '''
        return self.the_error_channel

    def create_filter_endpoint(self, selector):
        '''
        Creates a Filter Endpoint
        '''
        filter_endpoint = FilterEndpoint(selector)
        self.components.append(filter_endpoint)
        return filter_endpoint

    def start(self):
        '''
        Starts this PyIntegration.
        '''
        for component in self.components:
            try:
                component.start()
            except Exception as e:
                sys.stderr.write(str(e)) 

    def stop(self):
        '''
        Stops this PyIntegration.
        '''
        for component in self.components:
            try:
                component.stop()
            except Exception as e:
                sys.stderr.write(str(e)) 