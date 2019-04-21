import Queue
from MainServer_Client import MainServer_Client
from SQL_connection import SQL_connection
import thread


class MainServer():
    def __init__(self):
        self.client_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.client_communication = MainServer_Client(self.client_command, self.command_result)
        thread.start_new_thread(self.client_communication.main, ())
        self.client_command_def = {
            -1: self.disconnect,
            1: self.sign_up,
            2: self.sign_in}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter
        self.socket_username = {}  # socket:username
        self.sql_connection = SQL_connection()

    def disconnect(self, current_socket, msg_parameter):
        if current_socket in self.socket_username.keys():
            del self.socket_username[current_socket]

    def sign_up(self, current_socket, msg_parameter):
        print "main server: sign up:  " + str(msg_parameter)
        username, password = msg_parameter
        if self.sql_connection.check_username_taken(username):
            return [False]
        self.sql_connection.create_new_username(username, password)
        self.socket_username[current_socket] = username
        return [True]

    def sign_in(self, current_socket, msg_parameter):
        print "main server: sign in:  " + str(msg_parameter)
        username, password = msg_parameter
        if not self.sql_connection.check_user_legal(username, password):
            return [False]
        if username in self.socket_username.values():
            return [False]
        self.socket_username[current_socket] = username
        return [True]

    def main(self):
        while True:
            while self.client_command.empty():
                pass
            command = self.client_command.get()
            print "command: " + str(command)
            result = self.client_command_def[command[1][0]](command[0], command[1][1])
            print "result: " + str(result)
            print "\n"
            if command[1][0] != -1:
                self.command_result.put([command[0], [command[1][0], result]])


if __name__ == "__main__":
    a = MainServer()
    a.main()
