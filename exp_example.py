#!/usr/bin/python

from  manager import *
import numpy as np
import time
import sys
import matplotlib
import matplotlib.pyplot as plt
import math

def figure_config():
    font = {'weight': 'bold',
            'size': 12
            }
    matplotlib.rc('font', **font)

def plot_linechart(a, a_label, xlabel, title):
    f = plt.figure()
    plt.plot(range(len(a)), a, 'ro-', label=a_label)
    plt.legend()
    plt.xlabel(xlabel)
    plt.title(title)

    f.show()

def simulation(lamb, times):
    manager = EventManager(auto_next=True)
    # manager = EventManager(auto_next=False)
    manager.add_event(Event('Event1', np.random.exponential, scale=1.0/lamb))
    step = 0.1
    max_value = 10.0
    array_size = int(1.0*max_value/step)
    data = np.array([0]*array_size)
    for cnt in xrange(times):
        event = manager.next()
        d = manager.delta_ts()
        if d > step*array_size:
            continue
        index = int(1.0*d/step)
        data[index] = data[index] + 1
        # event.next()

    # plot
    f = plt.figure()
    x = np.arange(0, array_size*step, step)
    # step*prob * times = cnt
    # prob = cnt/times/step
    y = data*1.0/times/step
    plt.plot(x, y, 'ro-')
    plt.title("exp test")

    f.show()
    plt.show()

simulation(0.5, 1000000)
