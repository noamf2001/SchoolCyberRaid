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


def get_key_by_value(dict, search_value):
    for key, value in dict.items():
        if value == search_value:
            return key


class MainServer():
    def __init__(self, saving_path=""):
        self.socket_username = {}  # socket:username

        self.client_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_client = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.client_communication = MainServer_Client(self.client_command, self.command_result_client, saving_path)
        thread.start_new_thread(self.client_communication.main, ())
        self.client_command_def = {
            -1: self.disconnect_client,
            1: self.sign_up_client,
            2: self.sign_in,
            3: self.upload_file}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter

        self.valid_data_server = {"?": None}  # mac address : data server socket
        self.data_server_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_data_server = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.data_server_communication = MainServer_DataServer(self.data_server_command,
                                                               self.command_result_data_server, self.valid_data_server)
        thread.start_new_thread(self.data_server_communication.main, ())
        self.command_result_data_server_def = {
            -1: self.disconnect_data_server,
            1: self.sign_up_data_server}  # msg_type : method that take care of it, take as parameter: current
        # socket, msg_parameter

        self.sql_connection = SQL_connection()

    def disconnect_client(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]

    def disconnect_data_server(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]

    def sign_up_client(self, current_socket, msg_parameter):
        username, password = msg_parameter
        if self.sql_connection.check_username_taken(username):
            return [False]
        self.sql_connection.create_new_username(username, password)
        self.socket_username[current_socket] = username
        return [True]

    def sign_up_data_server(self, current_socket, msg_parameter):
        print "sign up data server!!!!!"
        self.sql_connection.add_data_server(get_key_by_value(self.valid_data_server, current_socket))
        return [None]

    def sign_in(self, current_socket, msg_parameter):
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
        print "file path: " + file_path

        parts_num, file_len, files_part_path = AlgorithmMain.create_parity_files(file_path)
        data_servers = self.sql_connection.get_all_data_server()
        if len(data_servers) == 0:
            print "not enough data server"
            return [False]
        division_part_data_server = AlgorithmMain.divide_parts_to_data_server(files_part_path, data_servers)
        for i in range(len(division_part_data_server)):
            for j in range(len(division_part_data_server[i][1])):
                self.data_server_command.put([self.valid_data_server[division_part_data_server[i][0]],
                                              [3, [division_part_data_server[i][1][j][
                                                   division_part_data_server[i][1][j].rfind("\\"):],
                                                   division_part_data_server[i][1][j]]]])
        return [True]

    def main(self):
        while True:
            if not self.client_command.empty():
                command_client = self.client_command.get()
                print "command client: " + str(command_client)
                result = self.client_command_def[command_client[1][0]](command_client[0], command_client[1][1])
                print "result: " + str(result) + "\n"
                if command_client[1][0] != -1:
                    self.command_result_client.put([command_client[0], [command_client[1][0], result]])
            if not self.command_result_data_server.empty():
                result_data_server = self.command_result_data_server.get()
                print "command data_server: " + str(result_data_server)
                result = self.command_result_data_server_def[result_data_server[1][0]](result_data_server[0],
                                                                                       result_data_server[1][1])
                print "result: " + str(result) + "\n"
                if result_data_server[1][0] != -1 and result_data_server[1][0] != 1:
                    self.data_server_command.put([result_data_server[0], [result_data_server[1][0], result]])


if __name__ == "__main__":
    a = MainServer(r"C:\Users\Sharon\Documents\school\cyber\Project\server_try")
    a.main()
    # a.upload_file(None, ["noam", r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename.txt"])
