# -*- coding: utf-8 -*-
import socket
import sys
from threading import Thread, Lock
from serverclient import Client
import time

sys.path.insert(1, '..//network')
from NetworkConstants import receive_codes, send_codes


class Server:
    def __init__(self, max_clients, port):
        
        self.max_clients = max_clients
        self.clients = []
        self.clientpid = 1 #0=server
        self.port = port
        self.socket = None
        self.running = False
        
    def inputs(self):
        while self.running:
            x=input("Server>")
            
            if "/help" in x:
                print("help coming soon LOL")
            
            if "/say" in x:
                text=x.replace("/say ", "")
                
                for players in self.clients:
                    players.clearbuffer()
                    players.writebyte(send_codes["chat"])
                    players.writestring("SERVER: "+text)
                    players.sendmessage()
            if "/test" in x:
                text=x.replace("/test ", "")
                for players in self.clients:
                    if players.name=="nick":
                        players.clearbuffer()
                        players.writebyte(send_codes["chat"])
                        players.writestring(text)
                        players.sendmessage()
            
    def start(self):
        #create new socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.bind(("",self.port))
            self.running = True
        except:
            print("Failed to bind socket- check to make sure server is not already running")
            sys.exit()
            
        #main loop
        self.input_thread = Thread(target = self.inputs)
        self.input_thread.setDaemon(True)
        self.input_thread.start()
        print("ready")
        while self.running:
            time.sleep(1/1000)
            
            self.socket.listen(self.max_clients)
            
            connection, address = self.socket.accept()
            print('Connected by', address)
            client = Client(connection, address, self, self.clientpid)
            client.start()
            self.clients.append(client)
            self.clientpid+=1
                
                
s = Server(32, 1337)
s.start()
