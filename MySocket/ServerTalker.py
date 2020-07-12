# coding=utf-8
import json
import socket

from MySocket.SocketConfig import ServerBasic, ClientBasic


class ServerTalker(socket.socket, ServerBasic):
    def __init__(self):
        super(ServerTalker, self).__init__()
        ServerBasic.__init__(self)
        self.bind_listen()

    def pop_clients(self):
        popped = []
        for name, client in self.clients_dict.items():
            name: str
            client: ClientHelper
            if not client.alive:
                popped.append((name, self.clients_dict.pop(name)))
        return popped

    def bind_listen(self):
        super(ServerTalker, self).bind(('0.0.0.0', 2004))
        self.listen(self.max_clients)

    def close(self):
        super(ServerTalker, self).close()
        client: ClientHelper
        for client in self.clients_dict.values():
            client.close()
        self.alive = False

    def get_client(self):
        client = ClientHelper(self.accept()[0])
        client_data: dict = json.loads(client.receive())  # data格式： {client_name: data_dict}
        client_name = client.name = list(client_data.keys())[0]
        self.clients_dict.update({client_name: client})  # 将客户端加入到客户端套接字字典中
        return client_name, client, client_data

    def receive_all(self) -> dict:
        get_dict = {}
        for name, client in self.clients_dict.items():
            client: ClientHelper
            get_dict[name] = json.loads(client.receive())
        self.pop_clients()
        return get_dict

    def all_send(self, data: bytes) -> list:
        get_list = []
        for name, client in self.clients_dict.items():
            client: ClientHelper
            get_list.append(client.once_send(data))
        return get_list

    def one_send(self, client_name: str, data: bytes) -> int:
        client: ClientHelper = self.clients_dict[client_name]
        return client.once_send(data)


class ClientHelper(ClientBasic):
    def __init__(self, client: socket.socket, name=''):
        super(ClientHelper, self).__init__()
        self.socket = client
        self.name = name


if __name__ == '__main__':
    a = ServerTalker()
    a.bind_listen()
    c2_name, c2, c2_data = a.get_client()
    get = b''
    try:
        get += c2.receive()
        a.all_send(get)
    finally:
        c2.close()
        a.close()
