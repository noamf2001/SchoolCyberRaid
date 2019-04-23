import socket
import select
from MainServer_DataServer_Protocol import MainServer_DataServer_Protocol
import Queue
from binascii import hexlify
PORT = 1345


class MainServer_DataServer():
    def __init__(self, data_server_command, command_result, valid_data_server):
        """
        :param data_server_command: empty queue
        :param command_result: empty queue
        """
        self.valid_data_server = valid_data_server
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', PORT))
        self.server_socket.listen(100)
        self.open_data_server_sockets = []
        self.msg_to_send = {}  # socket: msg to send
        self.sent_AES_key = set()  # socket
        self.main_server_data_server_protocol = MainServer_DataServer_Protocol()
        self.data_server_command = data_server_command  # queue: [socket, [msg_type, msg_parameters]]
        self.command_result = command_result  # queue: [socket, [msg_type, msg_parameters]]

    def disconnect(self, current_socket):
        print "disconnect!!"
        self.open_data_server_sockets.remove(current_socket)
        if current_socket in self.msg_to_send.keys():
            del self.msg_to_send[current_socket]
        self.data_server_command.put([current_socket, [-1, []]])

    def recv_msg(self, current_socket, first=False):
        msg_type, msg_parameters, connection_fail = self.main_server_data_server_protocol.recv_msg(current_socket,
                                                                                                   first)
        if connection_fail:
            self.disconnect(current_socket)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, current_socket, msg):
        connection_fail = self.main_server_data_server_protocol.send_msg(current_socket, msg)
        if connection_fail:
            self.disconnect(current_socket)
        return connection_fail

    def send_waiting_messages(self, wlist):
        for current_socket in wlist:
            if current_socket in self.msg_to_send.keys():
                connection_fail = self.send_msg(current_socket, self.msg_to_send[current_socket])
                if connection_fail:
                    continue
                del self.msg_to_send[current_socket]

    def get_msg_to_send(self):
        while not self.command_result.empty():
            msg_info = self.command_result.get()
            self.msg_to_send[msg_info[0]] = self.main_server_data_server_protocol.build(msg_info[1][0], msg_info[1][1])

    def main(self):
        while True:
            rlist, wlist, xlist = select.select([self.server_socket] + self.open_data_server_sockets,
                                                self.open_data_server_sockets, [])
            for current_socket in rlist:
                if current_socket is self.server_socket:
                    (new_socket, address) = self.server_socket.accept()
                    print "connect to data server"
                    if hexlify(new_socket.getsockname()[4]) in self.valid_data_server:
                        self.open_data_server_sockets.append(new_socket)
                    else:
                        new_socket.close()
                else:
                    if current_socket not in self.sent_AES_key:
                        self.sent_AES_key.add(current_socket)
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket, True)
                        print "msg type: " + str(msg_type)
                        print "msg parameter: " + str(msg_parameters)
                        if connection_fail:
                            print "connection fail"
                            continue
                        self.msg_to_send[current_socket] = self.main_server_data_server_protocol.build(0, [
                            self.main_server_data_server_protocol.export_AES_key()], msg_parameters[0])
                    else:
                        msg_type, msg_parameters, connection_fail = self.recv_msg(current_socket)
                        if connection_fail:
                            continue
                        self.data_server_command.put([current_socket, [msg_type, msg_parameters]])
            self.get_msg_to_send()
            self.send_waiting_messages(wlist)


if __name__ == '__main__':
    data_server_command1 = Queue.Queue()
    command_result1 = Queue.Queue()
    a = MainServer_DataServer(data_server_command1, command_result1)
    a.main()
