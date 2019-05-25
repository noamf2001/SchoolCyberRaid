import socket
import select
from Client_MainServer_Protocol import Client_MainServer_Protocol
import Queue

PORT = 1234
SERVER_IP = "127.0.0.1"


class ClientMainServer:
    def __init__(self, client_command, command_result, saving_path):
        """
        :param client_command: empty queue
        :param command_result: empty queue
        """
        self.my_socket = socket.socket()
        self.my_socket.connect((SERVER_IP, PORT))
        self.FAIL = False
        self.client_main_server_protocol = Client_MainServer_Protocol(self.my_socket, saving_path)
        self.client_command = client_command  # queue: [msg_type, msg_parameters]
        self.command_result = command_result  # queue: [msg_type, msg_parameters]
        self.client_command.put([0, [self.client_main_server_protocol.export_RSA_public_key()]])

    def recv_msg(self, rlist):
        """
        :param rlist: all the sockets that can recv a msg - the only option is the client socket

        """
        if self.my_socket in rlist:
            # recv msg - check if this is the first msg - there is not AES key
            msg_type, msg_parameters, connection_fail = self.client_main_server_protocol.recv_msg(self.client_main_server_protocol.AES_cipher is None)
            if connection_fail:
                self.FAIL = True
            else:
                # for regular msg - put result in queue for GUI
                # the first msg is the AES
                if self.client_main_server_protocol.AES_cipher is None:
                    self.client_main_server_protocol.create_AES_key(msg_parameters[0])
                else:
                    self.command_result.put([msg_type, msg_parameters])

    def send_waiting_messages(self, wlist):
        """
        :param wlist: the socket that can send msg - we only have one option - the client socket
        """
        if self.my_socket in wlist:
            # send msg if there is a msg in the command queue and connection and key exchanged was finished
            if not self.client_command.empty() and self.client_main_server_protocol.AES_cipher is not None:
                msg_info = self.client_command.get()
                msg_build = self.client_main_server_protocol.build(msg_info[0], msg_info[1])
                connection_fail = self.client_main_server_protocol.send_msg(msg_build)
                if connection_fail:
                    self.FAIL = True

    def main(self):
        """
        main client server connection class
        """
        while not self.FAIL:
            rlist, wlist, xlist = select.select([self.my_socket], [self.my_socket], [])
            self.recv_msg(rlist)
            self.send_waiting_messages(wlist)
        # disconnect from server
        self.command_result.put([-1,""])

