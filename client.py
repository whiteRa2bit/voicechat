import os
import sys
import socket
import threading

import pyaudio

from protocol import DataType, Protocol


class Client:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bufferSize = 4096
        self.connected = False
        
        self.name = input('Enter the name of the client --> ')
        
        while True:
            try:
                self.target_ip = input('Enter IP address of server --> ')
                self.target_port = int(input('Enter target port of server --> '))
                self.server = (self.target_ip, self.target_port)
                self.connectToServer()
                break
            except ():
                print("Couldn't connect to server...")

        self.chunk_size = 512
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            output=True, 
            frames_per_buffer=self.chunk_size
        )
        self.recording_stream = self.p.open(
            format=self.audio_format, 
            channels=self.channels, 
            rate=self.rate, 
            input=True, 
            frames_per_buffer=self.chunk_size
        )

        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()
        self.terminate()

    def receive_server_data(self):
        while self.connected:
            try:
                data, addr = self.s.recvfrom(1025)
                message = Protocol(datapacket=data)
                if message.DataType == DataType.ClientData:
                    self.playing_stream.write(message.data)
            except:
                pass

    def connectToServer(self):
        if self.connected:
            return True

        message = Protocol(dataType=DataType.Handshake, data=self.name.encode(encoding='UTF-8'))
        self.s.sendto(message.out(), self.server)

        data, addr = self.s.recvfrom(1025)
        datapack = Protocol(datapacket=data)

        if (addr==self.server and datapack.DataType==DataType.Handshake and 
        datapack.data.decode('UTF-8')=='ok'):
            print('Connected to server successfully!')
            print('Press Control + C to disconnect')
            self.connected = True
        return self.connected

    def send_data_to_server(self):
        while self.connected:
            try:
                data = self.recording_stream.read(512)
                message = Protocol(dataType=DataType.ClientData, data=data)
                self.s.sendto(message.out(), self.server)
            except:
                self._disconnect()

    def _disconnect(self):
        print("Try to disconnect")
        self.playing_stream.stop_stream()
        self.playing_stream.close()
        self.recording_stream.stop_stream()
        self.recording_stream.close()
        self.p.terminate()

        message = Protocol(dataType=DataType.Disconnect, data=self.name.encode(encoding='UTF-8'))
        self.s.sendto(message.out(), self.server)
        self.connected = False

    @staticmethod
    def terminate():
        print("Succesfuly disconnected")
        os._exit(1)


client = Client()
