#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration import PyIntegration


def test_empty_start_stop_does_not_hang():
    integration = PyIntegration()
    integration.start()
    integration.stop()
    
def test_non_empty_start_stop_does_not_hang():
    integration = PyIntegration()
    integration.create_point_to_point_channel()
    integration.start()
    integration.stop()