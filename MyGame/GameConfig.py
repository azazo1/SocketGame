# coding=utf-8
import json

import pygame
from MySocket.ClientTalker import ClientTalker
from MySocket.ServerTalker import ServerTalker


class GameConfig:
    fps = 60  # 帧率
    root_size = 700, 600  # 屏幕分辨率
    font_size = 50  # 字体大小
    font_path = None  # 字体文件位置


class GameBasic(GameConfig):
    def __init__(self):
        pygame.init()
        self.name = ''
        self.size = (50, 50)
        self.pos = (0, 0)
        self.color = (255, 255, 255)
        self.alive = True
        self.font = pygame.font.Font(self.font_path, self.font_size)  # TODO注意修改font文件位置

    def encode_data(self, characters: dict):
        data = json.dumps(characters).encode()
        return data

    def get_self_dict(self):
        return {
            self.name: {
                'rect': (*self.pos, *self.size),
                'color': self.color
            }
        }

    def check_self(self):
        if not self.alive:
            raise RuntimeError('This game had been closed!')

    def game_loop(self):
        print('Game started.')

    def close(self):
        print('Game closed.')
        self.alive = False
        pygame.quit()


class ServerGameBasic(GameBasic):
    def __init__(self):
        super(ServerGameBasic, self).__init__()
        self.server: ServerTalker = None

    def get_client(self):
        print('Waiting for connection.')
        self.server.get_client()

    def close(self):
        super(ServerGameBasic, self).close()
        self.server.close()


class ClientGameBasic(GameBasic):
    def __init__(self, name: str):
        super(ClientGameBasic, self).__init__()
        self.client: ClientTalker = None
        self.name: str = name

    def close(self):
        super(ClientGameBasic, self).close()
        self.client.close()
