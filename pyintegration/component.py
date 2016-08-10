#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Queue import Queue, Empty
import logging
from threading import Thread
import threading
import time

from pykka.actor import ActorRef
from pykka.exceptions import Timeout, ActorDeadError
from pykka.threading import ThreadingActor

from pyintegration.message import Message


logger = logging.getLogger('pyintegration')

class _MessageComponent(object):
    def __init__(self, queue=None):
        super(_MessageComponent, self).__init__()
        if queue is None:
            self.q = Queue()
        else:
            self.q = queue

    def size(self):
        return self.q.qsize()

    def _queue(self):
        return self.q

    def put(self, message):
        if isinstance(message, Message):
            self.q.put(message)
        else:
            raise ValueError("'message' must be a Message")

    @staticmethod
    def _MESSAGE_KEY():
        return 'message'

    @staticmethod
    def _to_message(message):
        if isinstance(message, dict) and _MessageComponent._MESSAGE_KEY() in message:
            return message
        else:
            return {_MessageComponent._MESSAGE_KEY() : str(message)}
           
    @staticmethod
    def _from_message(message):
        return message[ThreadingComponent._MESSAGE_KEY()]

class ThreadingComponent(_MessageComponent):
    '''
    Base class for all components of PyIntegration. This class implements
    PyKka's Actor model to provide a message-driven solution.
    '''
    def __init__(self, queue=None):
        super(ThreadingComponent, self).__init__(queue)
        self.consumer_thread = None
        self.producer_thread = None

    def start_actor(self, actor, actor_ref):
        return actor.start_acting(actor_ref)

    def consume(self, producer):
        '''
        Consumes from producer in a non-blocking fashion.
        '''
        if not isinstance(producer, ThreadingComponent):
            raise Exception('Invalid Producer')
        self.start_actor(ConsumerActor(self._queue()), ProducerActor.start(producer._queue()))

    def produce(self, consumer):
        '''
        Produces to consumer in a non-blocking fashion.
        '''
        if not isinstance(consumer, ThreadingComponent):
            raise Exception('Invalid Consumer')
        self.start_actor(ProducerActor(self._queue()), ConsumerActor.start(consumer._queue()))

class BaseActor(ThreadingActor, Thread):
    '''
    This actor, upon getting an 'ask' message, returns a messages from its queue.
    It will wait until a message is found in the queue.
    '''
    def __init__(self, queue):
        ThreadingActor.__init__(self)
        Thread.__init__(self)
        self.queue = queue
        self.running = False
        self._thread_event = None

    def start_acting(self, actor_ref):
        if not isinstance(actor_ref, ActorRef):
            raise Exception("Invalid ActorRef")
        self.actor_ref = actor_ref
        self.running = True
        self._thread_event = threading.Event()
        threading.Thread.start(self)

    def stopped(self):
        return self._thread_event.isSet()

    def on_start(self):
        '''
        ThreadingActor override
        '''
        pass
    
    def on_stop(self):
        '''
        ThreadingActor override
        '''
        self.stop_acting()

    def stop_acting(self):
        if self.running:
            self.running = False
            self._thread_event.set()

    def on_failure(self, exception_type, exception_value, traceback):
        '''
        ThreadingActor override
        '''
        logger.error('%s, %s, %s', exception_type, exception_value, traceback)
        self.stop_acting()

    def run(self):
        '''
        Runs while alive
        '''
        while self.running and self.actor_ref.is_alive():
            self.while_alive()

    def while_alive(self):
        pass

class ProducerActor(BaseActor):
    def while_alive(self):
        '''
        Sends messages to consumer
        '''
        try:
            the_message = self.queue.get(True, .0005)
            message = _MessageComponent._to_message(the_message)
            logger.info('%s sending message:%s', self, message)
            self.actor_ref.tell(message)
        except (ActorDeadError, Timeout):
            self.running = False
        except Empty:
            time.sleep(.001)

    def on_receive(self, message):
        '''
        Sends messages as a response
        '''
        try:
            the_message = self.queue.get(True, .0005)
            self.queue.task_done()
            logger.info('%s sending message:%s', self, the_message)
            return the_message
        except (ActorDeadError, Timeout):
            return None
        except Empty:
            time.sleep(.001)

class ConsumerActor(BaseActor):
    def while_alive(self):
        '''
        Receives messages from producer
        '''
        try:
            actor_message = self.actor_ref.ask({'message':'_m_'}, timeout=.0005)
            if actor_message is not None:
                logger.info('%s received message:%s', self, actor_message)
                self.queue.put(actor_message)
        except ActorDeadError:
            self.running = False
        except Timeout:
            self.running = False
            time.sleep(.001)

    def on_receive(self, message):
        '''
        Receives messages
        '''
        the_message = _MessageComponent._from_message(message)
        logger.info('%s received message:%s', self, the_message)
        self.queue.put(the_message)