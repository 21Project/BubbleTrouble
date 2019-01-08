import socket

data_payload = 2048
backlog = 2

class Server():
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