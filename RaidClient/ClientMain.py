import multiprocessing
import socket
import hashlib
from Client_MainServer import Client_MainServer
import Queue
import thread


class ClientMain():
    def __init__(self, saving_path):
        self.client_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.client_communication = Client_MainServer(self.client_command, self.command_result, saving_path)
        thread.start_new_thread(self.client_communication.main, ())
        self.username = None

    def get_command_result(self):
        """
        :return: [[msg_type,msg parameters],....]
        """
        result = []
        while not self.command_result.empty():
            result.append(self.command_result.get())
        return result

    def hash_password(self, password):
        """
        :param password: string
        :return: str of length 64 - the hash
        """
        return password
        #return hashlib.sha256(password).hexdigest()

    def check_legal_username(self, username):
        return len(username) >= 4 and len(username) <= 100

    def check_legal_password(self, password):
        return len(password) >= 4

    def sign_up(self, username, password):
        self.username = username
        if not self.check_legal_username(username) or not self.check_legal_password(password):
            return False
        self.client_command.put([1, [username, self.hash_password(password)]])
        while self.command_result.empty():
            pass
        return self.command_result.get()

    def sign_in(self, username, password):
        self.username = username
        self.client_command.put([2, [username, self.hash_password(password)]])
        while self.command_result.empty():
            pass
        return self.command_result.get()

    def upload_file(self, file_path):
        file_name = self.username + "$" + file_path[file_path.rfind("\\") + 1:]
        self.client_command.put([3, [file_name, file_path]])
        while self.command_result.empty():
            pass
        result = self.command_result.get()
        return result

    def get_file(self, file_name):
        file_name = self.username + "$"+file_name
        self.client_command.put([4,[file_name]])
        while self.command_result.empty():
            pass
        result = self.command_result.get()
        return result

    def delete_file(self, file_name):
        file_name = self.username + "$" + file_name
        self.client_command.put([5, [file_name]])
        while self.command_result.empty():
            pass
        result = self.command_result.get()
        return result

    def get_file_list(self):
        self.client_command.put([6, []])
        while self.command_result.empty():
            pass
        result = self.command_result.get()
        return result

if __name__ == '__main__':
    a = ClientMain(r"C:\Users\User\Documents\save")
    print a.sign_up("noam6", "hinoam")
    #print a.upload_file(r"C:\Users\User\Documents\file get\file_noam.txt")
    print a.get_file_list()
    print "finish"
    #print a.get_file(r"hahaha.txt")
    #print a.delete_file(r"hahaha.txt")
    print "finish second"
    while not a.client_communication.FAIL:
        pass