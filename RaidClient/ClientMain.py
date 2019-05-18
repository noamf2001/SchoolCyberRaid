import multiprocessing
import socket
import hashlib
from Client_MainServer import Client_MainServer
import Queue
import thread
import os


class ClientMain():
    def __init__(self, action_call_after_show, saving_path=os.getcwd()):
        self.client_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.client_communication = Client_MainServer(self.client_command, self.command_result, saving_path)
        thread.start_new_thread(self.client_communication.main, ())
        self.username = None
        self.action_call_after_show = action_call_after_show

    def set_saving_path(self, saving_path):
        self.client_communication.client_main_server_protocol.saving_path = saving_path

    def get_command_result(self):
        """
        :return: [[msg_type,msg parameters],....]
        """
        result = []
        while not self.command_result.empty():
            result.append(self.command_result.get())
        return result

    def check_legal_username(self, username):
        return True
        #return len(username) >= 4 and len(username) <= 20

    def check_legal_password(self, password):
        return True
        #return len(password) >= 4

    def sign_up(self, username, password):
        print "sign_up client main"
        self.username = username
        if not self.check_legal_username(username) or not self.check_legal_password(password):
            print "not legal"
            return False
        self.client_command.put([1, [username, password]])

    def sign_in(self, username, password):
        print "sign_in ClientMain: " + username + "  :  " + password
        self.username = username
        self.client_command.put([2, [username, password]])

    def upload_file(self, file_path):
        file_name = self.username + "$" + file_path[file_path.rfind("\\") + 1:]
        self.client_command.put([3, [file_name, file_path]])
        # while self.command_result.empty():
        #    pass
        # result = self.command_result.get()
        # return result

    def get_file(self, file_name):
        file_name = self.username + "$" + file_name
        self.client_command.put([4, [file_name]])

    def delete_file(self, file_name):
        file_name = self.username + "$" + file_name
        self.client_command.put([5, [file_name]])

    def get_file_list(self):
        self.client_command.put([6, []])

    def main_recv(self):
        while not self.client_communication.FAIL:
            if not self.command_result.empty():
                result = self.command_result.get()
                msg_type = result[0]
                msg_parameters = result[1]
                print "got msg: " + str(msg_type) + "\t\t"+str(msg_parameters)
                self.action_call_after_show[msg_type](msg_parameters)


if __name__ == '__main__':
    a = ClientMain()
    print a.sign_up("noam6", "hinoam")
    # print a.upload_file(r"C:\Users\User\Documents\file get\file_noam.txt")
    # print a.get_file_list()
    print "finish"
    print a.upload_file(r"C:\Users\Sharon\Documents\temp\file_try.txt")
    # print a.get_file(r"hahaha.txt")
    # print a.delete_file(r"hahaha.txt")
    print "finish second"
    while not a.client_communication.FAIL:
        pass
