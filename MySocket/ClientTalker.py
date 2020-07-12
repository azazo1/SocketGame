# coding=utf-8
import socket
from MySocket.SocketConfig import ClientBasic


class ClientTalker(ClientBasic):
    def __init__(self):
        super(ClientTalker, self).__init__()
        self.socket = socket.socket()

    def connect_server(self, ip: str = None, port: int = None):
        address = (ip, port) if ip and port else self.default_address  # 如果任意一个是空的则使用默认
        self.socket.connect(address)


if __name__ == '__main__':
    a = ClientTalker()
    try:
        a.connect_server()
        while 1:
            print(a.receive())
            if not a.alive:
                break
    finally:
        a.close()
