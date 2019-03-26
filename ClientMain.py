import multiprocessing
import socket
import hashlib

SERVERIP = "127.0.0.1"
PORT = 1234

class ClientMain():
    def __init__(self,SERVERIP,PORT):
        self.my_socket = socket.socket()
        self.my_socket.connect((SERVERIP, PORT))
