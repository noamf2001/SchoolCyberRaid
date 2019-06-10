import socket
import select
from MainServer_Client_Protocol import MainServer_Client_Protocol
import Queue


class MainServer_Client():
    def __init__(self, client_command, command_result, saving_path, port):
        """
        constructor
        :param client_command: empty queue
        :param command_result: empty queue
        """
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(100)
        self.open_client_sockets = []
        self.msg_to_send = {}  # socket: msg to send
        self.sent_AES_key = set()  # socket
        self.main_server_client_protocol = MainServer_Client_Protocol(saving_path)
        self.client_command = client_command  # queue: [socket, [msg_type, msg_parameters]]
        self.command_result = command_result  # queue: [socket, [msg_type, msg_parameters]]

    def disconnect(self, current_socket):
        """
        disconnect from client
        :param current_socket:
        """
        self.open_client_sockets.remove(current_socket)
        if current_socket in self.msg_to_send.keys():
            del self.msg_to_send[current_socket]
        self.client_command.put([current_socket, [-1, []]])

    def recv_msg(self, current_socket, first=False):
        """
        recv the msg from client :param current_socket: the socket the get the msg from :param first: if it is the
        first msg -> it is not encoded with the AES key, but this is the RSA public key :return: [msg type - by
                        protocol, msg parameters - depends on msg type -> [...], boolean if the connection was closed]
        """
        msg_type, msg_parameters, connection_fail = self.main_server_client_protocol.recv_msg(current_socket, first)
        if connection_fail:
            self.disconnect(current_socket)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, current_socket, msg):
        """
        send a specific msg to a specific client
        :param current_socket:
        :param msg:
        :return: boolean if the connection was closed
        """
        connection_fail = self.main_server_client_protocol.send_msg(current_socket, msg)
        if connection_fail:
            self.disconnect(current_socket)
        return connection_fail

    def send_waiting_messages(self, wlist):
        """
        send all the msg need to send in queue
        :param wlist:
        """
        for current_socket in wlist:
            if current_socket in self.msg_to_send.keys():
                #  and len(self.msg_to_send[current_socket]) > 0 and current_socket in self.sent_AES_key:
                connection_fail = self.send_msg(current_socket, self.msg_to_send[current_socket])
                if connection_fail:
                    continue
                del self.msg_to_send[current_socket]

    def get_msg_to_send(self):
        """
        extract msg from queue, and put the built msg in the dict
        """
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
                    if current_socket not in self.sent_AES_key:
                        self.sent_AES_key.add(current_socket)
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket, True)
                        if connection_fail:
                            continue
                        self.msg_to_send[current_socket] = self.main_server_client_protocol.build(0, [
                            self.main_server_client_protocol.export_AES_key()], msg_parameters[0])
                    else:
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket)
                        if connection_fail:
                            continue
                        self.client_command.put([current_socket, [msg_type, msg_parameters]])
            self.get_msg_to_send()
            self.send_waiting_messages(wlist)
