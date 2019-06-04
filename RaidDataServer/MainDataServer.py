import Queue
import thread
from DataServerMainServer import DataServerMainServer
import os
import socket
import re

# reverse dict
def get_key_by_value(dict, search_value):
    """
    severse dict action
    :param dict: the dictionary to look to
    :param search_value: the value
    :return:the first key who has that value
    """
    for key, value in dict.items():
        if value == search_value:
            return key


SERVER_IP = "127.0.0.1"
PORT = 1345


class DataServer:
    def __init__(self, saving_path=os.getcwd()):
        """
        constructor
        :param saving_path: the path to save the files - default it the current directory
        """
        self.saving_path = saving_path
        self.data_server_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result_data_server = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.main_server_communication = DataServerMainServer(self.data_server_command,
                                                              self.command_result_data_server, self.saving_path,
                                                              SERVER_IP,
                                                              PORT)
        thread.start_new_thread(self.main_server_communication.main, ())
        self.data_server_command_def = {
            -1: self.disconnect,
            3: self.upload_file,
            4: self.get_file,
            5: self.delete_file}  # msg_type : method that take care of it, take as parameter: current
        # socket, msg_parameter
        self.files = {}  # name: path

    def disconnect(self, msg_parameters):
        """
        disconnect rom server
        :param msg_parameters: no need
        """
        print "disconnect from server"
        exit()

    def upload_file(self, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file path]
        """
        self.files[msg_parameters[0][msg_parameters[0].rfind("\\") + 1:]] = msg_parameters[0]

    def get_regex_file_name(self, file_full_name):
        """
        build the regex
        :param file_full_name: the full name of the file that we are looking for its parts
        :return: the regax instance to look for the file parts
        """
        filename = file_full_name[file_full_name.find("$") + 1:]
        username = file_full_name[:file_full_name.find("$")]

        reg_part = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_(\d+)" + filename[filename.rfind("."):]
        reg_xor = username + r"[$]" + filename[:filename.rfind(".")] + r"_(\d+)_[-]1" + filename[filename.rfind("."):]
        reg = reg_part + r"|" + reg_xor

        reg = re.compile(reg)
        return reg

    def get_file(self, msg_parameters):
        """
        get all parts of a specific file
        :param msg_parameters: [file name]
        """
        reg = self.get_regex_file_name(msg_parameters[0])
        # get all file parts
        result_files = [file_part for file_part in self.files.keys() if reg.search(file_part) is not None]
        # send to server - do not open thread unless there is a file to
        if len(result_files) > 0:
            data_server_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
            command_result_data_server = Queue.Queue()  # queue: [msg_type, msg_parameters]
            send_file_parts = DataServerMainServer(data_server_command, command_result_data_server, "", SERVER_IP,
                                                   msg_parameters[1])
            thread.start_new_thread(send_file_parts.main, ())
            # send all the parts that the data server has
            for file_part in result_files:
                command_result_data_server.put([4, [file_part, self.files[file_part]]])

    def delete_file(self, msg_parameters):
        """
        delete all parts of that file
        :param msg_parameters: [file name]
        """
        reg = self.get_regex_file_name(msg_parameters[0])
        for file_part in self.files.keys():
            if reg.search(file_part) is not None:
                # remove from computer
                os.remove(self.files[file_part])
                # do not save that the data server has it
                del self.files[file_part]

    def main(self):
        """
        the main loop of the data server
        """
        while True:
            if not self.data_server_command.empty():
                command_data_server = self.data_server_command.get()
                if command_data_server[0] == 4:
                    thread.start_new_thread(self.get_file, args=command_data_server[1])
                else:
                    self.data_server_command_def[command_data_server[0]](command_data_server[1])


if __name__ == "__main__":
    a = DataServer(saving_path=r"C:\Users\Sharon\Documents\save_data_server")
    a.main()
