# coding=utf-8
from MyGame.ServerGame import ServerGame as Game
import pygame

class UserFacer:
    def __init__(self):
        pass

    def go(self):
        a = Game()
        try:
            a.get_client('b')
            a.game_loop()
        finally:
            a.close()


if __name__ == '__main__':
    UserFacer().go()
