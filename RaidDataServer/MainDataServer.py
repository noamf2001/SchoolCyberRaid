import Queue
import thread
from DataServer_MainServer import DataServer_MainServer
import os

"""
file name: username + $ + file original name
"""


def get_key_by_value(dict, search_value):
    for key, value in dict.items():
        if value == search_value:
            return key


class DataServer():
    def __init__(self, saving_path=""):
        self.data_server_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result_data_server = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.main_server_communication = DataServer_MainServer(self.data_server_command,
                                                               self.command_result_data_server, saving_path)
        thread.start_new_thread(self.main_server_communication.main, ())
        self.data_server_command_def = {
            3: self.upload_file}  # msg_type : method that take care of it, take as parameter: current
        # socket, msg_parameter
        self.files = {}  # name: path

    def upload_file(self, msg_parameters):
        """
        :param current_socket: the socket that getting it from
        :param msg_parameters: [file name, file path]
        """
        print "main server: upload file:  " + str(msg_parameters)
        self.files[msg_parameters[0]] = msg_parameters[1]
        return None

    def main(self):
        while not self.main_server_communication.FAIL:
            if not self.data_server_command.empty():
                command_data_server = self.data_server_command.get()
                print "command data_server: " + str(command_data_server)
                result = self.data_server_command_def[command_data_server[0]](command_data_server[1])
                print "result: " + str(result)
                print "\n"
                if command_data_server[0] != -1 and command_data_server[0] != 3:
                    self.command_result_data_server.put([command_data_server[0], result])


if __name__ == "__main__":
    a = DataServer(r"C:\Users\Sharon\Documents\school\cyber\Project\data_server_try")
    a.main()
