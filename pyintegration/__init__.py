#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from pyintegration.channel import ErrorChannel, PointToPointChannel


class PyIntegration(object):
    '''
    Python Enterprise Integration Framework.
    '''
    def __init__(self):
        self.channels = list()  

    def create_point_to_point_channel(self):
        '''
        Creates a Point-to-Point Channel.
        '''
        channel = PointToPointChannel()
        self.channels.append(channel)
        return channel

    def create_error_channel(self):
        '''
        Creates an Error Channel
        '''
        channel = ErrorChannel()
        self.channels.append(channel)
        return channel

    def start(self):
        '''
        Starts this PyIntegration.
        '''
        for component in self.channels:
            try:
                component.start()
            except Exception as e:
                sys.stderr.write(str(e)) 

    def stop(self):
        '''
        Stops this PyIntegration.
        '''
        for component in self.channels:
            try:
                component.stop()
            except Exception as e:
                sys.stderr.write(str(e)) 