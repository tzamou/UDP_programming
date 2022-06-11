import socket
import threading

class Server:
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sck.bind(('127.0.0.1', 5000))
        self.data = None
    def receved(self):
        while True:
            self.data, addr = self.sck.recvfrom(1024)
            if self.data!=b'':
                print(f'received:{self.data}')
            act=self.data.decode('utf-8')
            self.sck.sendto(act.encode('utf-8'),addr)


if __name__=="__main__":
    s = Server()
    td=threading.Thread(target=s.receved)
    td.setDaemon(True)
    td.start()
    while True:
        pass

