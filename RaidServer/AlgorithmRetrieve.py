import socket
import select
from AlgorithmMain import get_file_info
from MainServer_DataServer import MainServer_DataServer
import Queue
import thread
import os

"""
part file name:
filename_part number_if it is a parity file - the other part number, else -1
example:
namg_2_4

"""


class AlgorithmRetrieve():
    def __init__(self, port, num_of_parts, file_len, valid_data_server, optional_data_server, saving_path):
        self.stop_thread = False
        self.file_len = file_len
        self.open_client_sockets = []
        self.part_file = ["" for i in range(num_of_parts)]  # List[string] - the path of the files
        self.parity_parts = [set() for i in range(
            num_of_parts)]  # [set(xor parts that have connection to this part) for part i, 1<=i<= num_of_parts]

        self.valid_data_server = valid_data_server
        # self.optional_data_server = optional_data_server
        self.data_server_command = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.command_result_data_server = Queue.Queue()  # queue: [current_socket, [msg_type, msg_parameters]]
        self.data_server_communication = MainServer_DataServer(self.data_server_command,
                                                               self.command_result_data_server, self.valid_data_server,
                                                               optional_data_server,
                                                               saving_path, port)
        self.data_server_communication_thread_id = thread.start_new_thread(self.data_server_communication.main, (True,))

    def retrieve_file_part_generate_path(self, file_path1, file_path2):
        """
        :param file_path1: path of file part - can be regular part or parity part, can not be ""
        :param file_path2: path of file part - can be regular part or parity part, can not be ""
        :return: the file path that we an create
        """
        end_of_filename1, [file_part1_index1, file_part1_index2] = get_file_info(file_path1)
        end_of_filename2, [file_part2_index1, file_part2_index2] = get_file_info(file_path2)
        if file_part1_index2 == -1:
            file_index = file_part2_index1 if file_part1_index1 != file_part2_index1 else file_part2_index2
        else:
            file_index = file_part1_index1 if file_part2_index1 != file_part1_index1 else file_part1_index2
        file_path = file_path1[:end_of_filename1 + 1] + str(file_index) + "_" + "-1" + file_path1[
                                                                                       file_path1.rfind("."):]
        return file_path, file_index

    def retrieve_file_part(self, file_path1, file_path2):
        """
        :param file_path1: path of file part - can be regular part or parity part, can be ""
        :param file_path2: path of file part - can be regular part or parity part, can be ""
        one of those are parity, and the other is not, that means that if none of them is empty string, then it is possible to create file part (may be we already got it)
        :return: None, create file part if needed
        creating parity file is not needed (create parity <=> we have the both file parts that it can generate -> it is useless)
        """
        if file_path1 == "" or file_path2 == "":
            return
        file_path, file_index = self.retrieve_file_part_generate_path(file_path1, file_path2)
        if self.part_file[file_index] != "":
            return
        self.part_file[file_index] = file_path
        with open(file_path1, "rb") as f1:
            file1_data = bytearray(f1.read())
        with open(file_path2, "rb") as f2:
            file2_data = bytearray(f2.read())
        file_data = file1_data
        for i in range(len(file1_data)):
            file_data[i] = file_data[i] ^ file2_data[i]
        with open(file_path, "wb") as f:
            f.write(file_data)
        self.part_file[file_index] = file_path

    def add_file_path(self, file_path):
        """
        :param file_path: a path of file part to add
        """
        end_of_filename, [file_part_index1, file_part_index2] = get_file_info(file_path)
        if file_part_index2 == -1:
            self.part_file[file_part_index1] = file_path
            for parity_part in self.parity_parts[file_part_index1]:
                self.retrieve_file_part(file_path, parity_part)
        else:
            self.retrieve_file_part(self.part_file[file_part_index1], file_path)
            self.retrieve_file_part(self.part_file[file_part_index2], file_path)
            if file_path not in self.parity_parts[file_part_index1]:
                self.parity_parts[file_part_index1].add(file_path)
            if file_path not in self.parity_parts[file_part_index2]:
                self.parity_parts[file_part_index2].add(file_path)

    def is_finish(self):
        for part in self.part_file:
            if part == "":
                return False
        return True

    def connect_file(self):
        """
            is_finish() = True
            len(self.part_file) >= 1
            :return file path
        """
        file_part_path = self.part_file[0]
        end_of_filename, [file_part_index1, file_part_index2] = get_file_info(file_part_path)
        file_path = file_part_path[:end_of_filename] + file_part_path[file_part_path.rfind("."):]
        current_len = 0
        if os.path.isfile(file_path):
            os.remove(file_path)
        for file_part_path in self.part_file:
            with open(file_part_path, "rb") as fr:
                data = fr.read()
            os.remove(file_part_path)
            if current_len + len(data) > self.file_len:
                data = data[:self.file_len - current_len]
            else:
                current_len += len(data)
            with open(file_path, "ab") as fw:
                fw.write(data)
        return file_path

    def disconnect_data_server(self, current_socket):
        self.data_server_communication.stop_thread = True

    def main(self):
        while not self.stop_thread:
            if not self.command_result_data_server.empty():
                result_data_server = self.command_result_data_server.get()
                if result_data_server[1][0] == -1:
                    self.disconnect_data_server(result_data_server[0])
                else:
                    self.add_file_path(result_data_server[1][1][0])


if __name__ == '__main__':
    a = AlgorithmRetrieve(3, 3, 300)
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_2.txt")
    print a.part_file
    print a.parity_parts
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_0_1.txt")
    print a.part_file
    print a.parity_parts
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_-1.txt")
    print a.part_file
    print a.parity_parts
    a.connect_file()
