#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyintegration import PyIntegration


def test_empty_start_stop_does_not_hang():
    integration = PyIntegration()
    integration.start()
    integration.stop()
