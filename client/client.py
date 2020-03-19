# -*- coding: utf-8 -*-
import socket
import time
import sys
import struct
from threading import Thread
sys.path.insert(1, '..//network')
import Network
from NetworkConstants import receive_codes, send_codes


class Client:
    def __init__(self, ip, port, name):
        self.socket=None
        self.ip=ip
        self.port=port
        self.running = False
        
        self.buffer = Network.Buff()
        self.pid=-1
        
        self.name=name
    def sendmessage(self, buff=None, debuf=False):
        if buff == None:
            buff=self.buffer
        types = ''.join(buff.BufferWriteT)
        length=struct.calcsize("="+types)
        buff.BufferWrite[0]=length #set header length
        
        self.socket.send(struct.pack("="+types, *buff.BufferWrite))
        
    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.ip,self.port))
        except Exception as e:
            print(e)
            sys.exit()
        self.running = True
        print("connected")
        Thread(target=self.update,args=()).start()
        return self
    def update(self):
        self.sendping()
        #send join packet
        self.clearbuffer()
        self.writebyte(send_codes["join"])
        self.writestring(self.name)
        self.sendmessage()

        while self.running:
            time.sleep(1/1000)
            #send ping messages
            
            
            try:
                self.buffer.Buffer = self.socket.recv(1024)
                #self.buffer.Buffer0 = self.buffer.Buffer
                while(len(self.buffer.Buffer))>0:
                    packet_size = len(self.buffer.Buffer)
                    
                    msg_size = self.readushort() #read the header
                    
                    #if we have not gotten enough data, keep receiving
                    while(len(self.buffer.Buffer)+2<msg_size):
                        self.buffer.Buffer+=self.connection.recv(1024)
                        packet_size=len(self.buffer.Buffer)+2
                    
                    self.handlepacket()
                    
                    #pop the remaining data in the packet
                    while((packet_size-len(self.buffer.Buffer))<msg_size):
                        self.readbyte()
                        
            except ConnectionResetError:
                self.disconnect_user()
   
    def sendping(self):
        self.clearbuffer()
        self.writebyte(send_codes["ping"])
        self.sendmessage()
        
    def sendchat(self, chat):
        self.clearbuffer()
        self.writebyte(send_codes["chat"])
        self.writestring(chat)
        self.sendmessage()
        
    def handlepacket(self):
        event_id=self.readbyte()
        if event_id == receive_codes["ping"]:
            self.case_message_ping()
        if event_id == receive_codes["chat"]:
            self.case_message_chat()
        if event_id == receive_codes["join"]:
            self.case_message_join()
    def case_message_join(self):
        print(self.readstring() + " joined")
    def case_message_ping(self):
        #print("pinged")
        self.sendping()
    
    def case_message_chat(self):
        chat=self.readstring()
        print(str(chat))
    

    
    
    
    def clearbuffer(self):
        self.buffer.clearbuffer()
    def writebit(self,b):
        self.buffer.writebit(b)
    def writebyte(self,b):
        self.buffer.writebyte(b)
    def writestring(self,b):
        self.buffer.writestring(b)
    def writeint(self,b):
        self.buffer.writeint(b)
    def writedouble(self,b):
        self.buffer.writedouble(b)
    def writefloat(self,b):
        self.buffer.writefloat(b)
    def writeshort(self,b):
        self.buffer.writeshort(b)
    def writeushort(self,b):
        self.buffer.writeushort(b)
    def readstring(self):
        return self.buffer.readstring()
    def readbyte(self):
        return self.buffer.readbyte()
    def readbit(self):
        return self.buffer.readbit()
    def readint(self):
        return self.buffer.readint()
    def readdouble(self):
        return self.buffer.readdouble()
    def readfloat(self):
        return self.buffer.readfloat()
    def readshort(self):
        return self.buffer.readshort()
    def readushort(self):
        return self.buffer.readushort()
