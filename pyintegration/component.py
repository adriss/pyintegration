#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pykka.threading import ThreadingActor


class Component(object):
    def ref(self):
        return self.actor_ref
    
    def receive(self, message):
        raise Exception('Not Implemented')
    
    def start(self):
        self.actor_ref = ComponentActor.start(self)

    def stop(self):
        '''
        Stops this component
        '''
        self.actor_ref.stop()

    def send_to_ref(self, actor_ref, message):
        '''
        Sends a message to an actor reference.
        '''
        actor_ref.tell(message)

class ComponentActor(ThreadingActor):
    def __init__(self, receiver):
        super(ComponentActor, self).__init__()
        self.receiver = receiver

    def on_receive(self, message):
        self.receiver.receive(message)