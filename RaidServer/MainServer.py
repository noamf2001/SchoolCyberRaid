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
            1: self.sign_up}  # msg_type : method that take care of it, take as parameter: current socket, msg_parameter
        self.socket_username = {}  # socket:username
        self.sql_connection = SQL_connection()

    def sign_up(self, current_socket, msg_parameter):
        print "main server: sign up:  " + str(msg_parameter)
        username, password = msg_parameter
        if self.sql_connection.check_username_taken(username):
            return False
        self.sql_connection.create_new_username(username, password)
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
            self.command_result.put([command[0], [command[1][0], result]])


if __name__ == "__main__":
    a = MainServer()
    a.main()
