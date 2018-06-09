#!/usr/bin/python

import numpy as np
import time
import sys
from copy import copy
from functools import partial

np.random.seed(int(time.time()))

class Event:
    '''
    Event class is a random value generator producing next timestamp of the event.

    @param name  Name of the event
    @param dist  Function of numpy.random.RandomState
    @param kwarg  Parameters of the dist

    Notice: Use "kwargs" to assign dist. parameters!!
    '''
    def __init__(self, name, dist, **kwargs):
        self.name = name
        # check whether the dist is a function of np.random.RandomState
        assert dist.__self__.__class__ == np.random.RandomState
        self.gen = partial(dist, **kwargs)
        self.ts = self.gen()
        self.last_ts = 0

    def next(self):
        self.last_ts = self.ts
        self.ts += self.gen()
        return self.ts

    def init_ts(self, ts):
        '''
        Set the initial timestamp of the event.
        '''
        self.ts = self.ts + ts

    def delta_ts(self):
        '''
        Return the interval between two (same) events.
        '''
        return self.ts - self.last_ts
    
    def __str__(self):
        return '[{}]: {}'.format(self.name, self.ts)

    def __lt__(self, x):
        return self.ts < x.ts

    def __gt__(self, x):
        return self.ts > x.ts

    def __eq__(self, x):
        return self.ts == x.ts

class ExpireEvent(Event):
    '''
    ExpireEvent object will generate random value util expiration.

    @param expire  Expire time of the event
    '''
    def __init__(self, name, expire, dist, **kwargs):
        super(ExpireEvent, self).__init__(name, dist, **kwargs)
        # expire timestamp = first event timestamp + expire interval
        assert expire is not None
        self.expire = self.ts + expire

    def init_ts(self, ts):
        super(ExpireEvent, self).init_ts(ts)
        self.expire = self.expire + ts

class EventManager:
    '''
    EventManager class is able to select the next event according to the event timestamp.

    @param auto_next  The event will generate next timestamp automatically when call manager.next().

    Notice: auto_next will generate a little bit overhead
    '''
    def __init__(self, auto_next=False):
        self.event_list = []
        self.ts = 0 # timeline
        self.last_ts = 0

        self.auto_next = auto_next
        self.last_event = None

    def add_event(self, e):
        if not isinstance(e, Event):
            raise Exception('Added class is not subclass of Event')
        # start from manager's current timestamp
        e.init_ts(self.ts)
        self.event_list.append(e)

    def del_event(self, e):
        self.event_list.remove(e)

    def next(self):
        '''
        Return the event object with the smallest next timestamp.
        '''
        if self.auto_next and self.last_event:
            self.last_event.next()
        while True:
            min_event = min(self.event_list)
            self.last_ts = self.ts
            self.ts = min_event.ts
            if not isinstance(min_event, ExpireEvent) or min_event.ts < min_event.expire:
                break
            # expire event
            self.del_event(min_event)
            # FIXME: Not handle empty list condition...
            # Maybe we can create a class to implement dynamic input feature, and ensure the event_list won't be empty
            assert not self.event_list
        if self.auto_next:
            self.last_event = min_event
        return min_event

    def delta_ts(self):
        '''
        Return the interval between two events.
        '''
        return self.ts - self.last_ts

    def clear(self):
        del self.event_list
        self.event_list = []
        self.ts = 0
        self.last_ts = 0

