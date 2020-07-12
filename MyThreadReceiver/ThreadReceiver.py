# coding=utf-8
import json
import threading
import traceback
from socket import socket
import sys
from MySocket.ServerTalker import ClientHelper
from MyThreadReceiver.MessageTransfer import MessageTransfer


class Receiver(threading.Thread):
    def __init__(self, message_getter: socket, message: MessageTransfer, name: str):
        super(Receiver, self).__init__()
        self.message_getter = ClientHelper(message_getter, 'Getter')
        self.message = message
        self.running = True
        self.char_name = name
        self.setDaemon(True)

    def terminate(self):
        self.running = False
        self.message_getter.close()

    def run(self) -> None:
        while self.running and self.message_getter.alive:
            try:
                data = self.message_getter.receive()  # {clientname1: data1, clientname2: data2, ...}
                if not data:
                    continue
                data_dict = dict(**json.loads(data))
                for name, value in data_dict.items():
                    self.message.set(name, value)
            except Exception as e:
                exc_type, exc_value, exc_obj = sys.exc_info()
                traceback.print_tb(exc_obj)
                sys.stderr.write(f'{exc_type} {exc_value}\n')
                sys.stderr.flush()
        self.terminate()
