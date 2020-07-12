# coding=utf-8
import re


class SocketConfig:
    """套接字基本配置"""
    encoding = 'utf-8'  # 信息编码格式


class ClientConfig(SocketConfig):
    """客户端基本配置"""
    default_address = ('192.168.137.1', 2004)  # 默认客户端寻找主机地址


class ServerConfig(SocketConfig):
    """服务端基本配置"""
    max_clients = 5  # 主机最大接受客户端数量


class ServerBasic(ServerConfig):
    """服务端基本模型"""

    def __init__(self):
        self.alive = True
        self.clients_dict = {}


class ClientBasic(ClientConfig):
    """客户端基础模型"""

    def __init__(self):
        self.socket = None
        self.alive = True
        self.encoding = ClientConfig.encoding
        self.default_address = ClientConfig.default_address

    def close(self):
        self.socket.close()
        self.alive = False

    def once_send(self, data: bytes) -> int:
        length = f'{len(data)}:'.encode(self.encoding)
        data = length + data
        return self.socket.sendall(data)

    def receive(self) -> bytes:  # 接收完整信息，并检测socket可用性，自动切换存活状态
        com = re.compile('[0-9]')
        length = b''
        while 1:
            try:
                get: bytes = self.socket.recv(1)
                if get != b':' and not com.search(get.decode()):  # 除错区
                    return self.receive()  # 递归去除不在范围内的错误字节
            except Exception as e:  # 客户端断开
                self.close()
                return b''

            if not get:  # 客户端断开
                self.close()
                return b''

            length += get
            if b':' == get:  # 头消息结束
                length = length[:-1]
                break
        length = int(length)
        answer = self.socket.recv(length)
        while len(answer) < length:
            answer += self.socket.recv(1)
        return answer
