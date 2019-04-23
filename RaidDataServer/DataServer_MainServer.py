import socket
import select
from DataServer_MainServer_Protocol import DataServer_MainServer_Protocol
import Queue

PORT = 1345
SERVER_IP = "127.0.0.1"


class DataServer_MainServer():
    def __init__(self, data_server_command, command_result):
        """
        :param data_server_command: empty queue
        :param command_result: empty queue
        """
        self.my_socket = socket.socket()
        self.my_socket.connect((SERVER_IP, PORT))
        print "connected"
        self.FAIL = False
        self.data_server_main_server_protocol = DataServer_MainServer_Protocol(self.my_socket)
        self.data_server_command = data_server_command  # queue: [msg_type, msg_parameters]
        self.command_result = command_result  # queue: [msg_type, msg_parameters]
        self.data_server_command.put([0, [self.data_server_main_server_protocol.export_RSA_public_key()]])
        self.send_first_msg = False

    def recv_msg(self, rlist):
        if self.my_socket in rlist:
            print "start recv msg!!!"
            if self.data_server_main_server_protocol.AES_cipher is None:
                msg_type, msg_parameters, connection_fail = self.data_server_main_server_protocol.recv_msg(True)
            else:
                msg_type, msg_parameters, connection_fail = self.data_server_main_server_protocol.recv_msg()
            if connection_fail:
                print "connection fail"
                self.FAIL = True
            else:
                print "msg type: " + str(msg_type)
                print "msg parameter: " + str(msg_parameters)
                if self.data_server_main_server_protocol.AES_cipher is None:
                    self.data_server_main_server_protocol.create_AES_key(msg_parameters[0])
                else:
                    self.command_result.put([msg_type, msg_parameters])

    def send_waiting_messages(self, wlist):
        if self.my_socket in wlist:
            if not self.data_server_command.empty() and (
                    not self.send_first_msg or self.data_server_main_server_protocol.AES_cipher is not None):
                print "send_msg"
                if not self.send_first_msg:
                    self.send_first_msg = True
                msg_info = self.data_server_command.get()
                print "msg_info from queue: " + str(msg_info)
                msg_build = self.data_server_main_server_protocol.build(msg_info[0], msg_info[1])
                connection_fail = self.data_server_main_server_protocol.send_msg(msg_build)
                if connection_fail:
                    self.FAIL = True

    def main(self):
        while not self.FAIL:
            rlist, wlist, xlist = select.select([self.my_socket], [self.my_socket], [])
            self.recv_msg(rlist)
            self.send_waiting_messages(wlist)


if __name__ == '__main__':
    data_server_command = Queue.Queue()
    command_result = Queue.Queue()
    a = DataServer_MainServer(data_server_command, command_result)
    a.main()
