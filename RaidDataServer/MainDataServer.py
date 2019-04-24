import Queue
import thread
from DataServer_MainServer import DataServer_MainServer
import os
import socket
import re

"""
file name: username + $ + file original name
"""


def get_key_by_value(dict, search_value):
    for key, value in dict.items():
        if value == search_value:
            return key


SERVER_IP = "127.0.0.1"
PORT = 1345


class DataServer():
    def __init__(self, saving_path=""):
        self.data_server_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result_data_server = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.main_server_communication = DataServer_MainServer(self.data_server_command,
                                                               self.command_result_data_server, saving_path, SERVER_IP,
                                                               PORT)
        thread.start_new_thread(self.main_server_communication.main, ())
        self.data_server_command_def = {
            3: self.upload_file,
            4: self.get_file}  # msg_type : method that take care of it, take as parameter: current
        # socket, msg_parameter
        self.files = {}  # name: path

    def upload_file(self, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file path]
        """
        print "main server: upload file:  " + str(msg_parameters)
        self.files[msg_parameters[0][msg_parameters[0].rfind("\\") + 1:]] = msg_parameters[0]
        return [None]

    def get_file(self, msg_parameters):
        filename = msg_parameters[0][msg_parameters[0].find("$") + 1:]
        username = msg_parameters[0][:msg_parameters[0].find("$")]

        reg_part = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_(\d+)" + filename[filename.rfind("."):]
        reg_xor = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_[-]1" + filename[filename.rfind("."):]
        reg = reg_part + r"|" + reg_xor

        reg = re.compile(reg)
        result_files = [file_part for file_part in self.files.keys() if reg.search(file_part) is not None]
        print "the result file len: " + str(len(result_files))
        if len(result_files) > 0:
            data_server_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
            command_result_data_server = Queue.Queue()  # queue: [msg_type, msg_parameters]
            send_file_parts = DataServer_MainServer(data_server_command, command_result_data_server, "", SERVER_IP,
                                                    msg_parameters[1])
            thread.start_new_thread(send_file_parts.main, ())
            for file_part in result_files:
                command_result_data_server.put([4, [file_part, self.files[file_part]]])
            while not send_file_parts.FAIL:
                pass


    def main(self):
        while not self.main_server_communication.FAIL:
            if not self.data_server_command.empty():
                command_data_server = self.data_server_command.get()
                print "command data_server: " + str(command_data_server)
                result = self.data_server_command_def[command_data_server[0]](command_data_server[1])
                print "result: " + str(result)
                print "\n"
                #if command_data_server[0] != -1 and command_data_server[0] != 3:
                #    self.command_result_data_server.put([command_data_server[0], result])


if __name__ == "__main__":
    a = DataServer(r"C:\Users\Sharon\Documents\school\cyber\Project\data_server_try")
    a.main()
