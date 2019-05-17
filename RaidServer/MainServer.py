import Queue
from MainServer_Client import MainServer_Client
from MainServer_DataServer import MainServer_DataServer
from SQL_connection import SQL_connection
import thread
import AlgorithmMain
import os
from AlgorithmRetrieve import AlgorithmRetrieve
import random
import time
import threading
from find_all_mac_address_in_lan import get_mac_ip

"""
file name: username + $ + file original name
"""


def get_key_by_value(dict, search_value):
    for key, value in dict.items():
        if value == search_value:
            return key


PORT_DATA_SERVER = 1345
PORT_CLIENT = 1234


class MainServer:
    def __init__(self, sql_file_name, action_call_after_show,saving_path=os.getcwd()):
#        os.remove(sql_file_name)
        self.action_call_after_show = action_call_after_show
        self.sql_file_name = sql_file_name
        self.saving_path = saving_path
        self.ports_taken = set()
        self.ports_taken.add(PORT_CLIENT)
        self.ports_taken.add(PORT_DATA_SERVER)
        self.socket_username = {}  # socket:username

        self.client_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_client = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.client_communication = MainServer_Client(self.client_command, self.command_result_client, self.saving_path,
                                                      PORT_CLIENT)
        id_thread = thread.start_new_thread(self.client_communication.main, ())
        print "thread.start_new_thread(self.client_communication: " + str(id_thread)
        self.client_command_def = {
            -1: self.disconnect_client,
            1: self.sign_up_client,
            2: self.sign_in,
            3: self.upload_file,
            4: self.get_file,
            5: self.delete_file,
            6: self.get_file_list}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter

        self.valid_data_server = {}  # mac address : data server socket
        self.optional_data_server = get_mac_ip()  # ip : mac address of all the legal ones - the ones that are in this lan network
        self.optional_data_server["127.0.0.1"] ="02-00-4C-4F-4F-50"
        self.data_server_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_data_server = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.data_server_communication = MainServer_DataServer(self.data_server_command,
                                                               self.command_result_data_server, self.valid_data_server,
                                                               self.optional_data_server, PORT_DATA_SERVER)
        id_thread = thread.start_new_thread(self.data_server_communication.main, ())
        print "thread.start_new_thread(self.data_server_communication: " + str(id_thread)
        self.command_result_data_server_def = {
            -1: self.disconnect_data_server,
            1: self.sign_up_data_server, }  # msg_type : method that take care of it, take as parameter: current
        # socket, msg_parameter
        self.sql_file_name = sql_file_name

    def get_data_server(self):
        return self.valid_data_server.values()

    def disconnect_client(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]
        return None

    def disconnect_data_server(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]
        mac_address = get_key_by_value(self.valid_data_server, current_socket)
        self.sql_connection.delete_data_server(mac_address)
        self.action_call_after_show[-1](mac_address)
        return None

    def sign_up_client(self, current_socket, msg_parameter):
        print "sign up - client  - server"
        username, password = msg_parameter

        if self.sql_connection.check_username_taken(username):
            return [False]

        self.sql_connection.create_new_username(username, password)
        self.socket_username[current_socket] = username
        print str(self.socket_username)
        return [True]

    def sign_up_data_server(self, current_socket, msg_parameter):
        mac_address = get_key_by_value(self.valid_data_server, current_socket)
        self.sql_connection.add_data_server(mac_address)
        self.action_call_after_show[1](mac_address)
        return None

    def sign_in(self, current_socket, msg_parameter):
        print "sign in - client  - server"
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
        :param msg_parameters: [file path]
        :return [boolean]
        """
        print "start upload file in main server"
        sql_connection_upload_file = SQL_connection(self.sql_file_name)
        file_path = msg_parameters[0]
        username = file_path[file_path.rfind("\\") + 1:file_path.find("$", file_path.rfind("\\"))]
        parts_num, file_len, files_part_path = AlgorithmMain.create_parity_files(file_path)
        sql_connection_upload_file.save_user_file(username, file_path[file_path.find("$", file_path.rfind("\\")) + 1:],
                                                  parts_num, file_len)

        data_servers = sql_connection_upload_file.get_all_data_server()
        sql_connection_upload_file.close_sql()
        if len(data_servers) == 0:
            self.command_result_client.put([current_socket, [3, [file_path, False]]])
        division_part_data_server = AlgorithmMain.divide_parts_to_data_server(files_part_path, data_servers)
        print "next: " + str(self.valid_data_server)
        print "division_part_data_server : " + str(division_part_data_server)
        for i in range(len(division_part_data_server)):
            for j in range(len(division_part_data_server[i][1])):
                self.data_server_command.put([self.valid_data_server[division_part_data_server[i][0]],
                                              [3, [division_part_data_server[i][1][j]]]])
        #sql_connection_upload_file.get_data_server_files()
        self.command_result_client.put([current_socket, [3, [file_path,True]]])
        print "finish division of files in main server"
        #GUI
        self.action_call_after_show[3](file_path[file_path.rfind("\\") + 1:])

    def generate_port(self):
        port = random.randint(1000, 65535)
        while port in self.ports_taken:
            port = random.randint(1000, 65535)
        return port

    def get_file(self, current_socket, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file name]
        :return [file_name,file_path], [file_name,""] if file does not exists/could not get it
        """
        sql_connection_get_file = SQL_connection(self.sql_file_name)
        username = self.socket_username[current_socket]
        file_info = sql_connection_get_file.get_user_file_info(username,
                                                               msg_parameters[0][msg_parameters[0].find("$") + 1:])
        sql_connection_get_file.close_sql()
        if file_info is None:
            return [msg_parameters[0], ""]
        finish = False
        port = self.generate_port()
        retrieve_file = AlgorithmRetrieve(port, file_info[0], file_info[1], self.valid_data_server,
                                          self.optional_data_server, self.saving_path)
        thread.start_new_thread(retrieve_file.main, ())
        for i in range(3):
            for data_server_current_socket in self.data_server_communication.open_data_server_sockets:
                self.data_server_command.put([data_server_current_socket, [4, [msg_parameters[0], port]]])
            time_stop = 0
            while not finish and time_stop < 3:
                time.sleep(4)
                time_stop += 1
                finish = retrieve_file.is_finish()
            if finish:
                break
        if finish:
            file_path = retrieve_file.connect_file()
        else:
            file_path = ""
        self.command_result_client.put([current_socket, [4, [msg_parameters[0], file_path]]])

        return None

    def delete_file(self, current_socket, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file name]
        :return None
        """
        self.sql_connection.delete_user_file(self.socket_username[current_socket], msg_parameters[0])
        for data_server_current_socket in self.data_server_communication.open_data_server_sockets:
            self.data_server_command.put([data_server_current_socket, [5, [msg_parameters[0]]]])

        self.action_call_after_show[5](msg_parameters[0])
        return None

    def get_file_list(self, current_socket, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: []
        :return None
        """
        print "current_socket: " + str(self.socket_username)
        username = self.socket_username[current_socket]
        result = [file_name[0][file_name[0].rfind("$") + 1:] for file_name in
                  self.sql_connection.get_user_file_list(username)]
        return result

    def main(self):
        self.sql_connection = SQL_connection(self.sql_file_name)  # create it here so it will not be created by GUI thread
        while True:
            if not self.client_command.empty():
                command_client = self.client_command.get()
                #if sign up\in did not success
                if command_client[0] not in self.socket_username.keys() and command_client[1][0] > 2:
                    continue
                if command_client[1][0] == 3 or command_client[1][0] == 4 :
                    thread.start_new_thread(self.client_command_def[command_client[1][0]],
                                            (command_client[0], command_client[1][1]))
                else:
                    result = self.client_command_def[command_client[1][0]](command_client[0], command_client[1][1])
                    if result is not None:
                        self.command_result_client.put([command_client[0], [command_client[1][0], result]])
            if not self.command_result_data_server.empty():
                result_data_server = self.command_result_data_server.get()
                result = self.command_result_data_server_def[result_data_server[1][0]](result_data_server[0],
                                                                                       result_data_server[1][1])
                if result is not None:
                    self.data_server_command.put([result_data_server[0], [result_data_server[1][0], result]])


if __name__ == "__main__":
    db_name = "sec_db.sqlite"
    a = MainServer(db_name)
    a.main()
    # a.upload_file(None, ["noam", r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename.txt"])
