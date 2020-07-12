# coding=utf-8
from MyGame.ClientGame import ClientGame as Game
import pygame
import time

class UserFacer:

    def __init__(self):
        pass

    def go(self):
        a = Game('a'+str(time.time()))
        try:
            a.connect()
            a.game_loop()
        finally:
            a.close()


if __name__ == '__main__':
    UserFacer().go()
