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

class ThreadingComponent(object):
    '''
    Base class for all components of PyIntegration. This class implements
    PyKka's Actor model to provide a message-driven solution.
    '''
    def __init__(self, name=None, queue=None):
        super(ThreadingComponent, self).__init__()
        self.name = name
        if queue is None:
            self.q = Queue()
        else:
            self.q = queue

    def size(self):
        return self.q.qsize()

    def _queue(self):
        return self.q

    def get(self):
        self.q.get(True, .0005)
 
    def put(self, message):
        logger.debug(str('putting message: ' + str(message)))
        if isinstance(message, Message):
            self.q.put(message)
        else:
            raise ValueError("'message' must be a Message")

    @staticmethod
    def _MESSAGE_KEY():
        return 'message'

    @staticmethod
    def _to_message(message):
        if isinstance(message, dict) and ThreadingComponent._MESSAGE_KEY() in message:
            return message
        else:
            return {ThreadingComponent._MESSAGE_KEY() : str(message)}
           
    @staticmethod
    def _from_message(message):
        return message[ThreadingComponent._MESSAGE_KEY()]

    def start_actor(self, actor, actor_ref):
        logger.info('%s starting actor: %s', self, str(actor))
        return actor.start_acting(actor_ref)

    def consume(self, producer):
        '''
        Consumes from producer in a non-blocking fashion.
        '''
        if not isinstance(producer, ThreadingComponent):
            raise Exception('Invalid Producer')
        logger.info('%s creating consumer for producer: %s', self, str(producer))
        consumer_actor = ComponentActor(self._queue(), self.consume_while_alive, self.consume_on_receive)
        producer_actor_ref = ComponentActor.start(producer._queue(), self.not_produce_while_alive, self.produce_on_receive)
        logger.info('%s starting consumer actor: %s on producer actor ref: %s', self, str(consumer_actor), str(producer_actor_ref))
        self.start_actor(consumer_actor, producer_actor_ref)

    def produce(self, consumer):
        '''
        Produces to consumer in a non-blocking fashion.
        '''
        if not isinstance(consumer, ThreadingComponent):
            raise Exception('Invalid Consumer')
        logger.info('%s creating producer for consumer: %s', self, str(consumer))
        producer_actor = ComponentActor(self._queue(), self.produce_while_alive, self.produce_on_receive)
        consumer_actor_ref = ComponentActor.start(consumer._queue(), self.consume_while_alive, self.consume_on_receive)
        logger.info('%s starting producer actor: %s on consumer actor ref: %s', self, str(producer_actor), str(consumer_actor_ref))
        self.start_actor(producer_actor, consumer_actor_ref)


    def consume_while_alive(self, actor_ref, queue):
        '''
        Receives messages from producer
        '''
        try:
            actor_message = actor_ref.ask({'message':'_m_'}, timeout=.0005)
            if actor_message is not None:
                logger.info('%s received message:%s', self, actor_message)
                queue.put(actor_message)
        except ActorDeadError:
            self.running = False
        except Timeout:
            self.running = False
            time.sleep(.001)

    def consume_on_receive(self, message, queue):
        '''
        Receives messages
        '''
        the_message = ThreadingComponent._from_message(message)
        logger.info('%s consume_on_receive:%s', self, the_message)
        queue.put(the_message)

    def not_produce_while_alive(self, actor_ref, queue):
        '''
        Sends messages to consumer
        '''
        logger.info('%s NOT produce_while_alive:%s', self)

    def produce_while_alive(self, actor_ref, queue):
        '''
        Sends messages to consumer
        '''
        try:
            the_message = queue.get(True, .0005)
            message = ThreadingComponent._to_message(the_message)
            logger.info('%s produce_while_alive:%s', self, message)
            actor_ref.tell(message)
        except (ActorDeadError, Timeout):
            self.running = False
        except Empty:
            time.sleep(.001)

    def produce_on_receive(self, message, queue):
        '''
        Sends messages as a response
        '''
        try:
            the_message = queue.get(True, .0005)
            queue.task_done()
            logger.info('%s produce_on_receive:%s', self, the_message)
            return the_message
        except (ActorDeadError, Timeout):
            return None
        except Empty:
            time.sleep(.001)

    def __str__(self):
        if self.name is not None:
            return '[' + self.name + ']'
        else:
            return super.__str__(self)

class ComponentActor(ThreadingActor, Thread):
    '''
    This actor, upon getting an 'ask' message, returns a messages from its queue.
    It will wait until a message is found in the queue.
    '''
    def __init__(self, queue, component_while_alive, component_on_receive):
        ThreadingActor.__init__(self)
        Thread.__init__(self)
        self.queue = queue
        self.running = False
        self._thread_event = None
        self.component_while_alive = component_while_alive
        self.component_on_receive = component_on_receive

    def start_acting(self, actor_ref):
        logger.info('%s start_acting', self)
        if not isinstance(actor_ref, ActorRef):
            raise Exception("Invalid ActorRef")
        self.actor_ref = actor_ref
        self.running = True
        self._thread_event = threading.Event()
        threading.Thread.start(self)

    def stopped(self):
        return self._thread_event.isSet()

    def on_start(self):
        logger.info('%s on_start', self)
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
        logger.info('%s run', self)
        '''
        Runs while alive
        '''
        while self.running and self.actor_ref.is_alive():
            self.while_alive()

    def while_alive(self):
        self.component_while_alive(self.actor_ref, self.queue)
    
    def on_receive(self, message):
        '''
        Overrides Actor on_receive
        '''
        # logger.info('%s, on_receive:%s for:%s', self, message, self.component_on_receive.__name__)
        return self.component_on_receive(message, self.queue)
