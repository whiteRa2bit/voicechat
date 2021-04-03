import socket
import threading

from protocol import DataType, Protocol


class Server:
    def __init__(self):
            self.ip = socket.gethostbyname(socket.gethostname())
            while True:
                try:
                    self.port = int(input('Enter port number to run on --> '))

                    self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    self.s.settimeout(5)
                    self.s.bind((self.ip, self.port))

                    break
                except:
                    print("Couldn't bind to that port")

            self.clients = {}
            self.clientCharId = {}
            threading.Thread(target=self.receiveData).start()

    def receiveData(self):   
        print('Running on IP: '+self.ip)
        print('Running on port: '+str(self.port))
        
        while True:
            try:
                data, addr = self.s.recvfrom(1025)
                message = Protocol(datapacket=data)
                self.handleMessage(message, addr)
            except socket.timeout:
                pass

    def handleMessage(self, message, addr):
        print("Received {} message from {}".format(message.DataType, addr))
        if message.DataType == DataType.Handshake:
            if self.clients.get(addr, None) is None:
                try:
                    name = message.data.decode(encoding='UTF-8')

                    self.clients[addr] = name
                    self.clientCharId[addr] = len(self.clients)

                    print('{} has connected on {}!'.format(name, addr))
                    ret = Protocol(dataType=DataType.Handshake, data='ok'.encode(encoding='UTF-8'))
                    self.s.sendto(ret.out(), addr)
                except:
                    pass
        elif message.DataType == DataType.Disconnect:
            name = message.data.decode(encoding='UTF-8')

            if addr in self.clients:
                del self.clients[addr]
                del self.clientCharId[addr]
                print('{} on {} successfully disconnected'.format(name, addr))
            
            ret = Protocol(dataType=DataType.Disconnect, data='ok'.encode(encoding='UTF-8'))
            self.s.sendto(ret.out(), addr)
        elif message.DataType == DataType.ClientData:
            self.broadcast(addr, message)
        else:
            print("Unknown datatype: {}".format(message.DataType))

    def broadcast(self, sentFrom, data):
        data.head = self.clientCharId[sentFrom]
        for client in self.clients:
            if client != sentFrom:
                try:
                    self.s.sendto(data.out(), client)
                except:
                    pass

server = Server()
