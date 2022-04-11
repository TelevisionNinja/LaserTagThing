from socket import *
from threading import Thread

class UdpClientThread(Thread):
    def __init__(self, udpClient, handler):
        Thread.__init__(self)
        self.udpClient = udpClient
        self.handler = handler
        self.stopped = False
    
    def run(self):
        try:
            while not self.stopped:
                data = self.udpClient.s.recv(1024).decode("utf-8")
                self.handler.udpCallback(data)
        except Exception as e:
            print("Exception! (Ignore this if you're closing the window.)")
            print(e.message)

class UdpClient:
    def __init__(self, ip, port):
        self.s = socket(type = SOCK_DGRAM)
        self.s.bind((ip, port))