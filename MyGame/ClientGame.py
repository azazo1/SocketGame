# coding=utf-8
import time
import pygame
from MySocket.ClientTalker import ClientTalker
from MyGame.GameConfig import ClientGameBasic
from MyThreadReceiver.MessageTransfer import MessageTransfer
from MyThreadReceiver.ThreadReceiver import Receiver


class ClientGame(ClientGameBasic):
    def __init__(self, name: str):
        super(ClientGame, self).__init__(name)
        self.client = ClientTalker()

    def connect(self):
        self.client.connect_server()
        data_dict = self.get_self_dict()
        self.send_data(data_dict)

    def send_data(self, data_dict: dict):
        self.client.once_send(self.encode_data(data_dict))

    def game_loop(self):
        super(ClientGame, self).game_loop()
        pygame.init()
        root = pygame.display.set_mode(self.root_size)
        pygame.display.set_caption(self.name)
        message = MessageTransfer()
        getter_thread = Receiver(self.client.socket, message, self.name)
        getter_thread.start()
        while 1:
            events = pygame.event.get()
            if not self.client.alive:
                self.close()
                getter_thread.terminate()
                return 'error'
            for event in events:
                if event.type == pygame.QUIT:
                    self.close()
                    getter_thread.terminate()
                    return 'usual'
                if event.type == pygame.MOUSEMOTION:
                    self.pos = event.pos
                    self.send_data(self.get_self_dict())

            for name, data in message.dict.items():
                pygame.draw.rect(root, data['color'], data['rect'])

            pygame.display.update()
            root.fill((0, 0, 0))


if __name__ == '__main__':
    a = ClientGame(f'a{time.time()}')
    try:
        a.connect()
        print('get:', a.game_loop())
    finally:
        a.close()
