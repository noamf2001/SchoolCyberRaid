import multiprocessing
import socket
import hashlib
from Client_MainServer import ClientMainServer
import Queue
import thread
import os


class ClientMain:
    def __init__(self, action_call_after_show, saving_path=os.getcwd()):
        self.client_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.client_communication = ClientMainServer(self.client_command, self.command_result, saving_path)
        thread.start_new_thread(self.client_communication.main, ())
        self.username = None
        self.action_call_after_show = action_call_after_show

    def set_saving_path(self, saving_path):
        """
        :param saving_path: the path to save files
        set it as the path to save the files got from server
        """
        self.client_communication.client_main_server_protocol.saving_path = saving_path

    def get_command_result(self):
        """
        :return: [[msg_type,msg parameters],....]
        extract the commands from the queue
        """
        result = []
        while not self.command_result.empty():
            result.append(self.command_result.get())
        return result

    def check_legal_username(self, username):
        """
        :param username: the optional username
        :return: if the username is secure enough
        """
        return len(username) >= 4 and len(username) <= 20

    def check_legal_password(self, password):
        """
        :param password: the optional password vreated by the user
        :return: if the password is legal
        """
        return len(password) >= 4

    def sign_up(self, username, password):
        """
        :param username: the username
        :param password: the password
        if the username/password is not legal - put it the result queue
        """
        self.username = username
        if not self.check_legal_username(username) or not self.check_legal_password(password):
            self.command_result.put([1,[False]])
        self.client_command.put([1, [username, password]])

    def sign_in(self, username, password):
        """
        :param username:
        :param password:
        """
        self.username = username
        self.client_command.put([2, [username, password]])

    def upload_file(self, file_path):
        """
        :param file_path: the path of the file to send
        """
        file_name = self.username + "$" + file_path[file_path.rfind("\\") + 1:]  # build the file name to send
        self.client_command.put([3, [file_name, file_path]])

    def get_file(self, file_name):
        """
        :param file_name: the file name to get
        """
        file_name = self.username + "$" + file_name  # build the file name as specified
        self.client_command.put([4, [file_name]])

    def delete_file(self, file_name):
        """
        :param file_name: the file name to delete
        """
        file_name = self.username + "$" + file_name  # build the file name as specified
        self.client_command.put([5, [file_name]])

    def get_file_list(self):
        """
        just send to the server the request
        """
        self.client_command.put([6, []])

    def main_recv(self):
        while True:
            # if there is a result from server
            if not self.command_result.empty():
                result = self.command_result.get()
                msg_type = result[0]
                msg_parameters = result[1]
                # call the GUI to show the result
                self.action_call_after_show[msg_type](msg_parameters)

