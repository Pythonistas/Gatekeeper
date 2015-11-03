import sys
import zmq

context = zmq.Context()

subscriber = context.socket (zmq.SUB)
subscriber.connect("tcp://localhost:5556")
subscriber.setsockopt_string(zmq.SUBSCRIBE, "ANIMAL")

while True:
    message = subscriber.recv_string()
    print(message)