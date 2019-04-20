import socket
import select
from MainServer_Client_Protocol import MainServer_Client_Protocol
from Crypto.PublicKey import RSA
import Queue
from Crypto import Random
from Crypto.Cipher import AES


class MainServer_Client():
    def __init__(self, client_command, command_result):
        self.PORT = 1234
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', self.PORT))
        self.server_socket.listen(100)
        self.open_client_sockets = []
        self.msg_to_send = {}  # socket: msg to send
        self.asymmetric_key = {}  # socket: key
        self.main_server_client_protocol = MainServer_Client_Protocol()
        self.client_command = client_command  # queue: [socket, [msg_type, msg_parameters]]
        self.command_result = command_result  # queue: [socket: [msg_type, msg_parameters]]

    def disconnect(self, current_socket):
        pass

    def recv_msg(self, current_socket):
        msg_type, msg_parameters, connection_fail = self.main_server_client_protocol.recv_msg(current_socket)
        if connection_fail:
            self.disconnect(current_socket)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, current_socket, msg):
        connection_fail = self.main_server_client_protocol.send_msg(current_socket, msg)
        if connection_fail:
            self.disconnect(current_socket)
        return connection_fail

    def send_waiting_messages(self, wlist):
        for current_socket in wlist:
            if current_socket in self.msg_to_send.keys():
                connection_fail = self.send_msg(current_socket, self.msg_to_send[current_socket])
                if connection_fail:
                    continue

    def get_msg_to_send(self):
        while not self.command_result.empty():
            msg_info = self.command_result.get()
            self.msg_to_send[msg_info[0]] = self.main_server_client_protocol.build(msg_info[1][0], msg_info[1][1])

    def main(self):
        while True:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_client_sockets,
                                                self.open_client_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    (new_socket, address) = self.server_socket.accept()
                    self.open_client_sockets.append(new_socket)
                else:
                    if current_socket not in self.asymmetric_key.keys():
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket)
                        if connection_fail:
                            continue
                        client_asymmetric_key = msg_parameters[0]
                        self.asymmetric_key[current_socket] = client_asymmetric_key
                        self.msg_to_send[current_socket] = self.main_server_client_protocol.build(0, [])
                    else:
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket)
                        if connection_fail:
                            continue
                        self.client_command.put([current_socket, [msg_type, msg_parameters]])
            self.get_msg_to_send()
            self.send_waiting_messages(wlist)
