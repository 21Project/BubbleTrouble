import socket

class Client():
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
