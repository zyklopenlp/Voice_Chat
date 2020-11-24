# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:52:16 2020

@author: Jan
"""

import socket
import threading
from pydub import AudioSegment
import pydub
#import pyaudio
import pygame
from math import sqrt
from pygame.locals import *
import numpy as np
import math
import time
#from pydub.playback import play

volume = 0
#gain = np.array([[-10000000000,0,0],[0,-100000000000000,0],[0,0,-10000000000]],)

class get_gain():
    allpos = np.array([[0,0,0]])
    def recv_position():
        i=0
        connectionspos = []
        while True:
            clientpos_socket, addrpos = pos_socket.accept()
            connectionspos.append(clientpos_socket)
            i=i+1
            get_gain.allpos = np.append(get_gain.allpos,[[i,0,0]],axis=0)
            threading.Thread(target=get_gain.position, args=(clientpos_socket, addrpos,i,)).start()
    
                    
                    
    def position(clientpos_socket, addrpos,i):
        while True:
            try:
                pos=clientpos_socket.recv(1024*4)
                pos = np.frombuffer(pos)
                posX=pos[0]
                posY=pos[1]
                #print(posX)
                #lockgain.acquire()
                get_gain.allpos[i,0]=i
                get_gain.allpos[i,1]=posX
                get_gain.allpos[i,2]=posY
                #lockgain.release()
                #print(get_gain.allpos)
                pos_other=get_gain.allpos
                pos_other[0,0]=i
                posbyte=pos_other.tobytes()
                clientpos_socket.send(posbyte)
            except socket.error:
                clientpos_socket.close()
                #print('socket closed')
    
    def gain():
        while True:
            shape = get_gain.allpos.shape
            #print(shape)
            hight = shape[0]-1
            #print(hight)
            
            gain = np.zeros((hight,hight))
            for n in range(hight):
                for m in range(hight):
                    if n==m:
                        gain[n,m]=-1000000000000000000000000000
                    else:
                        d=math.sqrt((get_gain.allpos[n+1,1]-get_gain.allpos[m+1,1])**2+(get_gain.allpos[n+1,2]-get_gain.allpos[m+1,2])**2)
                        if d < 300:
                            gain[n,m]=0- (d**2)/100000
                        else:
                            gain[n,m]=-1000000000000000000000000000            
            #print(gain)
            global volume
            volume=gain
            time.sleep(1)
            #print(gain)

            
            
class connection():
    sounds ={}  
    def sound_out(c):
        g=0
        #gain=np.array([[-10000000000,-1000000000,0],[0,-100000000000000,0],[0,0,-10000000000]],)
        global volume
        gain=volume        
        #print(gain)
        if len(connection.sounds)==len(connections):
            try:
                #print(gain[c,g])
                lockgain.acquire()
                sound_out_c= connection.sounds[str(g)].apply_gain(gain[c,g])
                for g in range(len(connections)-1):
                    s=connection.sounds[str(g+1)].apply_gain(gain[c,g+1])
                    sound_out_c = sound_out_c.overlay(s)
                #print(c,g)
                lockgain.release()
                return sound_out_c
            except:
                print('Error 2')
        else:
            pass

    
    
    def handle_client(client_socket,addr,c):
        lockgain.acquire()
        connection.sounds[str(c)]=AudioSegment.empty()
        lockgain.release()
        while True:
            try:
                data = client_socket.recv(1024*4)                        
            except socket.error:
                client_socket.close()
            try:
                lockgain.acquire()
                connection.sounds[str(c)] = AudioSegment(data=data, sample_width=2, frame_rate=44100, channels=1)
                #print(connection.sounds)
                lockgain.release()
                
                audioout=connection.sound_out(c)
                connection.broadcast(client_socket, audioout)
            except:
                print('Error 1')
                
    
    def broadcast(sock, audio_send_kom):
        for client in connections:
            if client == sock:
                try:
                    #client=sock
                    audio_send = audio_send_kom.raw_data
                    client.send(audio_send)
                except:
                    pass
                    #print('no audio sent')
        

distance = 0
lockgain = threading.Lock()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
server_socket.bind((ip, 1337))
server_socket.listen(50)
connections = []
pos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pos_socket.bind((ip ,4242))
pos_socket.listen(50)

threading.Thread(target=get_gain.recv_position).start()
threading.Thread(target=get_gain.gain).start()

c=-1
while True:
    client_socket, addr = server_socket.accept()
    connections.append(client_socket)
    c=c+1
    time.sleep(1)
    threading.Thread(target=connection.handle_client,args=(client_socket, addr,c,)).start()
    



    

      


    
    
    


            
        

 
           
            
