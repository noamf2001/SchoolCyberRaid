import socket
import select
from DataServerMainServerProtocol import DataServerMainServerProtocol


class DataServerMainServer:
    def __init__(self, data_server_command, command_result, saving_path, SERVER_IP, PORT):
        """
        :param data_server_command: empty queue
        :param command_result: empty queue
        """
        self.my_socket = socket.socket()
        self.port = PORT
        self.my_socket.connect((SERVER_IP, PORT))
        self.FAIL = False
        self.data_server_main_server_protocol = DataServerMainServerProtocol(self.my_socket, saving_path)
        self.data_server_command = data_server_command  # queue: [msg_type, msg_parameters]
        self.command_result = command_result  # queue: [msg_type, msg_parameters]
        self.command_result.put([0, [self.data_server_main_server_protocol.export_RSA_public_key()]])
        self.send_first_msg = False

    def recv_msg(self, rlist):
        if self.my_socket in rlist:
            if self.data_server_main_server_protocol.AES_cipher is None:
                msg_type, msg_parameters, connection_fail = self.data_server_main_server_protocol.recv_msg(True)
            else:
                msg_type, msg_parameters, connection_fail = self.data_server_main_server_protocol.recv_msg()
            if connection_fail:
                self.FAIL = True
            else:
                if self.data_server_main_server_protocol.AES_cipher is None:
                    self.data_server_main_server_protocol.create_AES_key(msg_parameters[0])
                else:
                    self.data_server_command.put([msg_type, msg_parameters])

    def send_waiting_messages(self, wlist):
        if self.my_socket in wlist:
            if not self.command_result.empty() and (
                    not self.send_first_msg or self.data_server_main_server_protocol.AES_cipher is not None):
                if not self.send_first_msg:
                    self.send_first_msg = True
                msg_info = self.command_result.get()
                msg_build = self.data_server_main_server_protocol.build(msg_info[0], msg_info[1])
                connection_fail = self.data_server_main_server_protocol.send_msg(msg_build)
                if connection_fail:
                    self.FAIL = True

    def main(self):
        """
        the main loop that recv and send msg
        """
        while not self.FAIL:
            rlist, wlist, xlist = select.select([self.my_socket], [self.my_socket], [])
            self.recv_msg(rlist)
            self.send_waiting_messages(wlist)
        self.data_server_command.put([-1,[]])

