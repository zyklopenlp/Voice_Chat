# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:51:31 2020

@author: Jan
"""

import socket
import pyaudio
import threading
import time
import pygame
from pygame.locals import *
import numpy as np


def send_data_to_server():
    while True:
        try:
            data = recording_stream.read(1024*4)
            client_socket.sendall(data)
        except:
            pass
        
def receive_server_data():
    while True:
        try:
            audioout = client_socket.recv(1024*4)
            playing_stream.write(audioout)
        except:
            pass        
     
def GUI_out():
    W, H = 800, 600
    FPS  = 60
    SCHWARZ = ( 0, 0, 0)
    WEISS   = ( 255, 255, 255)
    
    spielaktiv = True
    
    posX = W/2
    posY = H/2
    VX = 0
    VY = 0
    a=10
    
    fenster = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Voice Chat")
    clock = pygame.time.Clock()
    
    while spielaktiv:
        for event in pygame.event.get():
            if event.type == QUIT:
                spielaktiv = False
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    VY = -a
                elif event.key == K_DOWN:
                    VY = a
                elif event.key == K_RIGHT:
                    VX = a
                elif event.key == K_LEFT:
                    VX = -a
                elif event.key == K_ESCAPE:
                    spielaktiv = False
                    
            if event.type == KEYUP:
                if event.key == K_UP or K_w or K_DOWN or K_s:
                    VX = 0
                if event.key == K_RIGHT or K_s or K_LEFT or K_a:
                    VY = 0
        if VX != 0:
            posX += VX
        elif VY != 0:
            posY += VY
        
        
        pos = np.array([posX,posY])
        pos.tobytes()
        clientpos_socket.send(pos)   
        allpos=clientpos_socket.recv(1024)
        posall = np.frombuffer(allpos, dtype="int32")
        #print(posall)
        
        fenster.fill(WEISS)
        
        for p in range(int(len(posall)/3-1)):
            i=posall[0]
            if i != p+1:
                X=posall[p*3+4]
                Y=posall[p*3+5]
                pygame.draw.ellipse(fenster, SCHWARZ, [X, Y, 5, 5])
        
        pygame.draw.ellipse(fenster, SCHWARZ, [posX, posY, 5, 5])
        pygame.display.flip()
        clock.tick(FPS)
    

channels = 1
rate = 44100
chunk_size = 1024*4
audio_format = pyaudio.paInt16


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_addr = ('192.168.56.1', 1337)
client_socket.connect(server_addr)
clientpos_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientpos_socket.connect(('192.168.56.1', 4242))
p = pyaudio.PyAudio()
playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)


receive_thread = threading.Thread(target=receive_server_data)
send_thread = threading.Thread(target=send_data_to_server)

receive_thread.start()
send_thread.start()

threading.Thread(target=GUI_out()).start()

while True:
    #client_socket.send(bytes('Hallo', 'utf8'))
    time.sleep(10)

    
    