#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys


class PyIntegration(object):
    '''
    Python Enterprise Integration Framework.
    '''
    def __init__(self):
        self.components = list()

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