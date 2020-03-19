from client import Client
import time
from threading import Thread

class Player:
    def __init__(self, name):
        self.name=name
        self.client=Client("127.0.0.1",1337, self.name).start()
        self.running=True
    def start(self):
        self.inputs()
        return self
    def inputs(self):
        while self.running:
            x=input("client>")
            self.client.sendchat(x)

name=input("name: ")
player=Player(name).start()
