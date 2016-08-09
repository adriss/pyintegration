#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pykka.threading import ThreadingActor
from pyintegration.message import Message
from Queue import Queue, Empty
import threading
import time
from pykka.exceptions import Timeout, ActorDeadError
from pykka.actor import ActorRef
import logging

logger = logging.getLogger('pyintegration')

class Component(object):
    '''
    Base class for all components of PyIntegration. This class implements
    PyKka's Actor model to provide a message-driven solution.
    '''
    def ref(self):
        return self.actor_ref
    
    def receive(self, message):
        raise Exception('Not Implemented')
    
    def start(self):
        self.actor_ref = _ComponentActor.start(self)

    def stop(self):
        '''
        Stops this component
        '''
        self.actor_ref.stop()

    def send_to_ref(self, actor_ref, message):
        if not isinstance(message, Message):
            raise Exception("Invalid Message")
        '''
        Sends a message to an actor reference.
        '''
        actor_ref.tell(_ComponentActor.to_message(message))

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

    def consume(self, producer):
        '''
        Consumes from producer in a non-blocking fashion.
        '''
        if not isinstance(producer, ThreadingComponent):
            raise Exception('Invalid Producer')
        self.consumer_thread = ConsumerThread(self._queue(), producer)
        self.consumer_thread.start()

    def produce(self, consumer):
        '''
        Produces to consumer in a non-blocking fashion.
        '''
        if not isinstance(consumer, ThreadingComponent):
            raise Exception('Invalid Consumer')
        #self.consumer_thread = ConsumerThread(self._queue(), self)
        #self.consumer_thread.start()

        self.producer_thread = ProducerThread(self._queue(), consumer)
        self.producer_thread.start()

    def _produce(self, message):
        self.producer.tell(ThreadingComponent._to_message(message))

    def _producer(self, thread):
        '''
        Creates a Producer to allow this component distribute messages.
        '''
        return ProducerActor.start(self._queue(), thread)

    def _consumer(self, thread):
        '''
        Creates a Consumer to allow this component receive messages.
        '''
        return ConsumerActor.start(self._queue(), thread)

class BaseActor(ThreadingActor):
    '''
    This actor, upon getting an 'ask' message, returns a messages from its queue.
    It will wait until a message is found in the queue.
    '''
    def __init__(self, queue, thread):
        super(BaseActor, self).__init__()
        self.queue = queue
        self.thread = thread

    def on_start(self):
        pass

    def on_stop(self):
        self.thread.stop()

    def on_failure(self, exception_type, exception_value, traceback):
        logger.error('%s, %s, %s', exception_type, exception_value, traceback)
        self.thread.stop()

class ProducerActor(BaseActor):
    def on_receive(self, message):
        '''
        Produces a message, if any available.
        '''
        if self.queue.empty():
            return None
        the_message = self.queue.get()
        self.queue.task_done()
        logger.info('%s sending message:%s', self, the_message)
        return the_message

class ConsumerActor(BaseActor):
    def on_receive(self, message):
        '''
        All messages received are placed in the queue.
        '''
        the_message = _MessageComponent._from_message(message)
        logger.info('%s received message:%s', self, the_message)
        self.queue.put(the_message)

class BaseThread(threading.Thread):
    def __init__(self):
        self.running = True
        self._stop = threading.Event()
        threading.Thread.__init__(self)

    def stop(self):
        self.running = False
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet()

    def start(self):
        threading.Thread.start(self)

class ProducerThread(BaseThread):
    def __init__(self, queue, consumer):
        self.queue = queue
        self.consumer = consumer
        BaseThread.__init__(self)

    def run(self):
        consumer_actor = self.consumer._consumer(self)
        if not isinstance(consumer_actor, ActorRef):
            raise Exception("Can't produce to consumer")
        while self.running and consumer_actor.is_alive():
            try:
                the_message = self.queue.get(False)
                message = _MessageComponent._to_message(the_message)
                consumer_actor.tell(message)
            except (ActorDeadError, Timeout):
                self.running = False
            except Empty:
                time.sleep(2)

class ConsumerThread(BaseThread):
    def __init__(self, queue, producer):
        self.queue = queue
        self.producer = producer
        BaseThread.__init__(self)

    def run(self):
        producer = self.producer._producer(self)
        while self.running and producer.is_alive():
            try:
                actor_message = producer.ask({'message':'_m_'})
                if actor_message is not None:
                    logger.info('%s received message:%s', self, actor_message)
                    self.queue.put(actor_message)
            except ActorDeadError:
                self.running = False
            except Timeout:
                self.running = False

class _ComponentActor(ThreadingActor):
    def __init__(self, receiver):
        super(_ComponentActor, self).__init__()
        self.receiver = receiver

    @staticmethod
    def MESSAGE_KEY():
        return 'message'

    @staticmethod
    def to_message(message):
        if isinstance(message, dict) and _ComponentActor.MESSAGE_KEY() in message:
            return message
        else:
            return {_ComponentActor.MESSAGE_KEY() : message}
            
    @staticmethod
    def from_message(message):
        return message[_ComponentActor.MESSAGE_KEY()]


    def on_failure(self, exception_type, exception_value, traceback):
        logger.error('Failure %s', traceback)

    def on_receive(self, message):
        self.receiver.receive(self.from_message(message))