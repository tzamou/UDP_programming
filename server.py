import socket
import threading

class Server:
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#建立socketsocket.AF_INET為IPv4 socket.SOCK_DGRAM為UDP連線
        self.sck.bind(('127.0.0.1', 5000))#選擇Host 跟port
        self.data = None
    def receved(self):
        while True:
            self.data, addr = self.sck.recvfrom(1024)#監聽來自客戶端的訊息
            if self.data!=b'':#如果訊息不是空字串的話就列印出來
                print(f'received:{self.data}')
            act=self.data.decode('utf-8')#把訊息解碼
            self.sck.sendto(act.encode('utf-8'),addr)#解碼後編碼再傳回客戶端


if __name__=="__main__":
    s = Server()
    td=threading.Thread(target=s.receved)#開啟執行序進行監聽
    td.setDaemon(True)#主執行緒結束後此執行緒也會結束
    td.start()
    while True:
        pass

