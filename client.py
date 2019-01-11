# Echo client program
import socket
import konfiguracija

poruka_za_konekciju = ''

OTHER_PORT = 0
MY_SERVER_HOST = ''
MY_SERVER_PORT = 0
OTHER_HOST = ''

def client_connect_function(text):
    HOST = '192.168.100.218'  # The remote host
    PORT = 50005        # The same port as used by the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #text2send = 'Hello world š đ č ć ž Здраво Свете'
        s.sendall(text.encode('utf8'))
        text1 = ''

        #bin = s.recv(1024)
        #text1 += str(bin, 'utf-8')
            # if not bin or len(bin) < 1024:
            #     break
        while text1 == '':
            text1 = receive_client(s)

        poruka_za_konekciju = text1
        print(poruka_za_konekciju)
        OTHER_HOST, OTHER_PORT, MY_SERVER_HOST, MY_SERVER_PORT = razdvoj(poruka_za_konekciju)
        print('Received {0}' .format(text1))
        return  OTHER_HOST, OTHER_PORT, MY_SERVER_HOST, MY_SERVER_PORT

def razdvoj(text):
    pomocna1 = text

    pomocna = pomocna1.split('|')
    pomocna[0] = pomocna[0].strip('(')
    pomocna[0] = pomocna[0].strip(')')
    pom_niz = pomocna[0].split(',')
    OTHER_HOST = str(pom_niz[0].strip("'"))
    OTHER_PORT = int(pom_niz[1].strip()) + 1
    pomocna[1] = pomocna[1].strip('(')
    pomocna[1] = pomocna[1].strip(')')
    pom_niz1 = pomocna[1].split(',')
    MY_SERVER_HOST = str(pom_niz1[0].strip("'"))
    MY_SERVER_PORT = int(pom_niz1[1].strip()) + 1

    print(OTHER_HOST)
    print(OTHER_PORT)
    print(MY_SERVER_HOST)
    print(MY_SERVER_PORT)

    return OTHER_HOST, OTHER_PORT, MY_SERVER_HOST, MY_SERVER_PORT


def receive_client(s):
    data = ''
    while True:
        bin = s.recv(1024)
        data += str(bin, 'utf8')
        if not bin or len(bin) < 1024:
            break
    return data


