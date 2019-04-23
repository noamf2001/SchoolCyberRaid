import multiprocessing
import socket
import hashlib
from Client_MainServer import Client_MainServer
import Queue
import thread


class ClientMain():
    def __init__(self):
        self.client_command = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.command_result = Queue.Queue()  # queue: [msg_type, msg_parameters]
        self.client_communication = Client_MainServer(self.client_command, self.command_result)
        thread.start_new_thread(self.client_communication.main, ())

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
        if not self.check_legal_username(username) or not self.check_legal_password(password):
            return False
        self.client_command.put([1, [username, self.hash_password(password)]])
        while self.command_result.empty():
            pass
        return self.command_result.get()

    def sign_in(self, username, password):
        self.client_command.put([2, [username, self.hash_password(password)]])
        while self.command_result.empty():
            pass
        return self.command_result.get()

    def upload_file(self, file_path):
        file_name = file_path[file_path.rfind("\\") + 1:]
        self.client_command.put([3, [file_name, file_path]])


if __name__ == '__main__':
    a = ClientMain()
    print a.sign_up("noam", "passwordofnoam")
