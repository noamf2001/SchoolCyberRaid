import socket
import select
from MainServer_DataServer_Protocol import MainServer_DataServer_Protocol

PORT = 1345


class MainServer_DataServer:
    def __init__(self, data_server_command, command_result_data_server, connected_data_server, optional_data_server,
                 saving_path, port=PORT):
        """
        :param data_server_command: empty queue: server -> data server
        :param command_result_data_server: empty queue: data server -> client
        """
        self.stop_thread = False
        self.connected_data_server = connected_data_server
        self.optional_data_server = optional_data_server
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(100)
        self.open_data_server_sockets = []
        self.msg_to_send = {}  # socket: [msg to send no 1, msg to send no 2,....]
        self.sent_AES_key = set()  # socket
        self.main_server_data_server_protocol = MainServer_DataServer_Protocol(saving_path)
        self.data_server_command = data_server_command  # queue: [socket, [msg_type, msg_parameters]]
        self.command_result_data_server = command_result_data_server  # queue: [socket, [msg_type, msg_parameters]]

    def disconnect(self, current_socket):
        """
        if data server was disconenct
        :param current_socket:
        """
        self.open_data_server_sockets.remove(current_socket)
        if current_socket in self.msg_to_send.keys():
            del self.msg_to_send[current_socket]
        self.command_result_data_server.put([current_socket, [-1, []]])

    def recv_msg(self, current_socket, first=False):
        """
        :param rlist: all the sockets that can recv a msg - the only option is the data server ocket
        """
        msg_type, msg_parameters, connection_fail = self.main_server_data_server_protocol.recv_msg(current_socket,
                                                                                                   first)
        if connection_fail:
            self.disconnect(current_socket)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, current_socket, msg):
        """
        send a specific msg to the socket
        :param current_socket: the socket to send to
        :param msg: the raw msg t send
        :return: boolean if the conenction fails
        """
        connection_fail = self.main_server_data_server_protocol.send_msg(current_socket, msg)
        if connection_fail:
            self.disconnect(current_socket)
        return connection_fail

    def send_waiting_messages(self, wlist):
        """
        send the msg needed
        :param wlist: all the socket that can send a msg
        """
        for current_socket in wlist:
            if current_socket in self.msg_to_send.keys() and len(
                    self.msg_to_send[current_socket]) > 0 and current_socket in self.sent_AES_key:
                msg = self.msg_to_send[current_socket][0]
                connection_fail = self.send_msg(current_socket, msg)
                if connection_fail:
                    continue
                self.msg_to_send[current_socket] = self.msg_to_send[current_socket][1:]

    def get_msg_to_send(self):
        """
        get from queue msg, and build it, and put it in dict
        """
        while not self.data_server_command.empty():
            msg_info = self.data_server_command.get()
            self.msg_to_send[msg_info[0]].append(
                self.main_server_data_server_protocol.build(msg_info[1][0], msg_info[1][1]))

    def main(self, get_file=False):
        """
        main loop to get msg from data server
        :param get_file: if this is to gather file parts
        """
        while not self.stop_thread:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_data_server_sockets,
                                                self.open_data_server_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    (new_socket, address) = self.server_socket.accept()
                    if address[0] in self.optional_data_server.keys():
                        self.open_data_server_sockets.append(new_socket)
                        if not get_file:
                            self.connected_data_server[self.optional_data_server[address[0]]] = new_socket
                            self.command_result_data_server.put([new_socket, [1, []]])
                        self.msg_to_send[new_socket] = []
                    else:
                        new_socket.close()
                else:
                    if current_socket not in self.sent_AES_key:
                        self.sent_AES_key.add(current_socket)
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket, True)
                        if connection_fail:
                            continue
                        self.msg_to_send[current_socket].insert(0, self.main_server_data_server_protocol.build(0, [
                            self.main_server_data_server_protocol.export_AES_key()], msg_parameters[0]))
                    else:
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket)
                        if connection_fail:
                            continue
                        self.command_result_data_server.put([current_socket, [msg_type, msg_parameters]])
            self.get_msg_to_send()
            self.send_waiting_messages(wlist)
        self.server_socket.close()
