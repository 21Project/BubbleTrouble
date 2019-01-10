import socket

data_payload = 2048
backlog = 1

class Server_igra():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((ip, port))
        self.sock.listen(backlog)

    def receive(self):
        data = None
        self.client, address = self.sock.accept()
        data = self.client.recv(data_payload).decode()
        return data

    def shutdown(self):
        self.sock.close()

class Client_igra():
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(20)
        try:
            self.sock.connect((ip, port))
        except socket.timeout:
            print('Timeout at connect')

    def send(self, message):
        try:
            self.sock.sendall(message.encode())
        except socket.timeout:
            print('Timeout at send')

    def shutdown(self):
        self.sock.close()

def send(msg, OTHER_HOST, OTHER_PORT):
    client = Client_igra(OTHER_HOST, OTHER_PORT)
    client.send(msg)
    client.shutdown()