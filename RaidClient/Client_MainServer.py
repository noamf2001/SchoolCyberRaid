import socket
import select
from Client_MainServer_Protocol import Client_MainServer_Protocol
from Crypto.PublicKey import RSA
import Queue
from Crypto import Random
from Crypto.Cipher import AES

PORT = 1234
SERVER_IP = "127.0.0.1"


class Client_MainServer():
    def __init__(self, client_command, command_result):
        self.my_socket = socket.socket()
        self.my_socket.connect((SERVER_IP, PORT))
        self.FAIL = False
        self.client_main_server_protocol = Client_MainServer_Protocol(self.my_socket)
        self.client_command = client_command  # queue: [msg_type, msg_parameters]
        self.command_result = command_result  # queue: [msg_type, msg_parameters]
        self.AES_key = None
        self.client_command.push([0,[]])

    def recv_msg(self, rlist):
        if self.my_socket in rlist:
            msg_type, msg_parameters, connection_fail = self.client_main_server_protocol.recv_msg
            if connection_fail:
                self.FAIL = True
            else:
                if self.AES_key is None:
                    self.AES_key = msg_parameters[0]
                    self.client_main_server_protocol.create_AES_key(self.AES_key)
                else:
                    self.command_result.put([msg_type, msg_parameters])

    def send_waiting_messages(self, wlist):
        if self.my_socket in wlist:
            if not self.client_command.empty():
                msg_info = self.client_command.get()
                msg_build = self.client_main_server_protocol.build(msg_info[1][0], msg_info[1][1])
                connection_fail = self.client_main_server_protocol.send_msg(msg_build)
                if connection_fail:
                    self.FAIL = True

    def main(self):
        while not self.FAIL:
            rlist, wlist, xlist = select.select([self.my_socket], [self.my_socket], [])
            self.recv_msg(rlist)
            self.send_waiting_messages(wlist)
