from client import *

def send(msg, OTHER_HOST, OTHER_PORT):
    client = Client(OTHER_HOST, OTHER_PORT)
    client.send(msg)
    client.shutdown()