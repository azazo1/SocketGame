# coding=utf-8
from threading import Thread
import pygame
from MySocket.ServerTalker import ServerTalker, ClientHelper
from MyGame.GameConfig import ServerGameBasic
from MyThreadReceiver.MessageTransfer import MessageTransfer
from MyThreadReceiver.ThreadReceiver import Receiver


class ClientReceiver(Thread):
    def __init__(self, server_socket: ServerTalker, message: MessageTransfer):
        super().__init__()
        self.server = server_socket
        self.message = message
        self.receivers = {}
        self.running = True
        self.setDaemon(True)

    def terminate(self):
        self.running = False
        for i in self.receivers.values():
            i: Receiver
            i.terminate()

    def run(self) -> None:
        while self.running:
            name, client, data = self.server.get_client()
            client: ClientHelper
            print(f'Get a Client named {name}.')
            receiver = Receiver(client.socket, self.message, name)
            receiver.start()
            self.receivers.update({name: receiver})


class ServerGame(ServerGameBasic):
    def __init__(self):
        super(ServerGame, self).__init__()
        self.name = 'server'
        self.server = ServerTalker()
        self.clock = pygame.time.Clock()
        self.message = MessageTransfer()
        self.client_getter = ClientReceiver(self.server, self.message)

    def close(self):
        super(ServerGame, self).close()
        self.client_getter.terminate()

    def game_loop(self):
        super(ServerGame, self).game_loop()
        pygame.init()
        self.client_getter.start()
        root = pygame.display.set_mode(self.root_size)
        while self.alive:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.close()
                    return
                if event.type == pygame.MOUSEMOTION:
                    self.pos = event.pos
                    self.message.set(self.name, self.get_self_dict()[self.name])
                    pass
            root.fill((0, 0, 0))
            self.server.all_send(self.encode_data(self.message.get_all()))

            for name, data in self.message.dict.items():
                pygame.draw.rect(root, data['color'], data['rect'])

            self.clock.tick(self.fps)
            pygame.display.update()


if __name__ == '__main__':
    a = ServerGame()
    try:
        a.game_loop()
    finally:
        a.close()
