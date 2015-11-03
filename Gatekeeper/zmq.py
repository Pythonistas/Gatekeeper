from Gatekeeper import app
from flask import Flask

import zmq

context = zmq.Context()
publisher = context.socket(zmq.PUB)
bound = False

def publish(topic, msg):
    # bind on demand. this allows the debug-'restart with stat' functionality
    # to work.
    global bound
    if not bound:
        publisher.bind("tcp://*:{0}".format(app.config['ZMQ_PUB_PORT']))
        bound = True

    publisher.send_string("{0} {1}".format(topic, msg))