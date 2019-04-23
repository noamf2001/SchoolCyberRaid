import Queue
from MainServer_Client import MainServer_Client
from MainServer_DataServer import MainServer_DataServer
from SQL_connection import SQL_connection
import thread
import AlgorithmMain
import os

"""
file name: username + $ + file original name
"""


class MainServer():
    def __init__(self):
        self.client_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_client = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.client_communication = MainServer_Client(self.client_command, self.command_result_client)
        thread.start_new_thread(self.client_communication.main, ())
        self.client_command_def = {
            -1: self.disconnect_client,
            1: self.sign_up,
            2: self.sign_in}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter
        self.socket_username = {}  # socket:username

        self.valid_data_server = set()
        self.data_server_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_data_server = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.data_server_communication = MainServer_DataServer(self.data_server_command,
                                                               self.command_result_data_server, self.valid_data_server)
        thread.start_new_thread(self.data_server_communication.main, ())
        self.data_server_command_def = {
            -1: self.disconnect_data_server}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter

        self.sql_connection = SQL_connection()

    def disconnect_client(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]

    def disconnect_data_server(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]

    def sign_up(self, current_socket, msg_parameter):
        print "main server: sign up:  " + str(msg_parameter)
        username, password = msg_parameter
        if self.sql_connection.check_username_taken(username):
            return [False]
        self.sql_connection.create_new_username(username, password)
        self.socket_username[current_socket] = username
        return [True]

    def sign_in(self, current_socket, msg_parameter):
        print "main server: sign in:  " + str(msg_parameter)
        username, password = msg_parameter
        if not self.sql_connection.check_user_legal(username, password):
            return [False]
        if username in self.socket_username.values():
            return [False]
        self.socket_username[current_socket] = username
        return [True]

    def upload_file(self, current_socket, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file name, file path]
        """
        print "main server: upload file:  " + str(msg_parameters)
        # file_path = msg_parameters[1][:msg_parameters[1].rfind("\\") + 1] + self.socket_username[current_socket] + \
        #            msg_parameters[0]
        file_path = msg_parameters[1]
        parts_num, file_len, file_part_path = AlgorithmMain.create_parity_files()



    def main(self):
        while True:
            if not self.client_command.empty():
                command_client = self.client_command.get()
                print "command client: " + str(command_client)
                result = self.client_command_def[command_client[1][0]](command_client[0], command_client[1][1])
                print "result: " + str(result)
                print "\n"
                if command_client[1][0] != -1:
                    self.command_result_client.put([command_client[0], [command_client[1][0], result]])
            if not self.data_server_command.empty():
                command_data_server = self.data_server_command.get()
                print "command data_server: " + str(command_data_server)
                result = self.data_server_command_def[command_data_server[1][0]](command_data_server[0],
                                                                                 command_data_server[1][1])
                print "result: " + str(result)
                print "\n"
                if command_data_server[1][0] != -1:
                    self.command_result_client.put([command_data_server[0], [command_data_server[1][0], result]])


if __name__ == "__main__":
    a = MainServer()
    a.upload_file(None, ["noam", r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename.txt"])
