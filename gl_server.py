import socket
import  pygame
import sys
from pygame.locals import *
from collections import OrderedDict
import threading

data_payload = 2048

#pygame.init()
#pygame.mouse.set_visible(True)

#screen_server = pygame.display.set_mode((400, 400))
#font_server = pygame.font.SysFont("monospace", 30)

class Glavni_Server():
    def __init__(self, ip, port):
        self.klijenti = []
        self.klijenti_soketi = []
        self.klijenti_turnir = []
        self.klijenti_turnir_soketi = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.listen(2)
        self.client = None



    def receive(self):
        data = ''
        while True:
            bin = self.client.recv(1024)
            data += str(bin, 'utf8')
            if not bin or len(bin) < 1024:
                break
        return data

    def shutdown(self):
        self.sock.close()

    def obradi_poruku(self):
        try:
            data = self.receive()
            if data == "dva_igraca":
                del self.klijenti_turnir[-1]
                del self.klijenti_turnir_soketi[-1]
                print('Server got {0}'.format(data))
                if len(self.klijenti) == 2:
                    self.razmeni_adrese(0,1)
                    del self.klijenti[0:2]
                    del self.klijenti_soketi[0:2]
                    print("zavrsava tred_drugi")
                    #self.client.close()
                    #sys.exit()
            elif data == "igraj_turnir":
                del self.klijenti[-1]
                del self.klijenti_soketi[-1]
                print('Server got {0}'.format(data))
                if len(self.klijenti) == 4:
                    self.razmeni_adrese(0,1)
                    self.razmeni_adrese(2,3)
                    del self.klijenti[0:4]
                    del self.klijenti_soketi[0:4]
                    print("zavrsava tred_drugi")
        except:
            self.client.close()
            print("Connection closed")
            # Quit the thread.
            sys.exit()



    def razmeni_adrese(self, index_prvog, index_drugog):
        klijent1 = ''
        klijent2 = ''
        klijent1 += str(self.klijenti[index_prvog])
        print(klijent1)
        klijent2 += str(self.klijenti[index_drugog])
        print(klijent2)
        pomocna = klijent1
        klijent1 += "|"
        klijent1 += klijent2
        klijent2 += "|"
        klijent2 += pomocna
        self.klijenti_soketi[index_drugog].sendall(klijent1.encode('utf8'))
        self.klijenti_soketi[index_prvog].sendall(klijent2.encode('utf8'))


adr = socket.gethostname()
server = Glavni_Server('', 50005)

while True:

    try:
        print("cekaju se klijenti")
        server.client, address = server.sock.accept()
        server.klijenti.insert(len(server.klijenti),address)
        server.klijenti_soketi.insert(len(server.klijenti_soketi),server.client)
        server.klijenti_turnir.insert(len(server.klijenti_turnir),address)
        server.klijenti_turnir_soketi.insert(len(server.klijenti_turnir_soketi),address)
        listener = threading.Thread(target = server.obradi_poruku)
        listener.start()
        print("stoji i dalje")
    except:
        print("nema klijenata")