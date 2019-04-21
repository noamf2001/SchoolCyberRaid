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

    def hash_password(self, password):
        return password

    def check_legal_username(self, username):
        return True

    def check_legal_password(self, password):
        return True

    def sign_up(self, username, password):
        if not self.check_legal_username(username) or not self.check_legal_password(password):
            return False
        self.client_command.put([1, [username, self.hash_password(password)]])
        while self.command_result.empty():
            pass
        return self.command_result.get()

if __name__ == '__main__':
    a = ClientMain()
    print a.sign_up("noam", "passwordofnoam")