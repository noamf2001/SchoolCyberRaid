import socket
import select
import DsProtocol

"""
part file name:
filename_part number_if it is a parity file - the other part number, else -1
example:
namg_2_4

"""


class AlgorithmRetrieve():
    def __init__(self, port, num_of_parts):
        self.server_socket = socket.socket()
        self.server_socket.bind(('0.0.0.0', port))
        self.open_client_sockets = []
        self.part_file = [None for i in range(num_of_parts)]  # type: List[None]
        self.part_file_found = [False for i in range(num_of_parts)]  # type: List[bool]

    @staticmethod
    def retrieve_file_part_generate_path(file_path1, file_path2):
        start_of_filename = file_path1.rfind("\\") + 1
        end_of_filename = file_path1.rfind("_", start_of_filename, file_path1.rfind("_"))
        file_part1_index1 = int(file_path1[end_of_filename + 1: file_path1.find("_", end_of_filename + 1)])
        file_part2_index1 = int(file_path2[end_of_filename + 1: file_path2.find("_", end_of_filename + 1)])
        file_part1_index2 = int(file_path1[file_path1.find("_", end_of_filename + 1) + 1: file_path1.rfind(".")])
        file_part2_index2 = int(file_path2[file_path1.find("_", end_of_filename + 1) + 1: file_path2.rfind(".")])
        if file_part1_index2 == -1:
            file_index = file_part2_index1 if file_part1_index1 != file_part2_index1 else file_part2_index2
        else:
            file_index = file_part1_index1 if file_part2_index1 != file_part1_index1 else file_part1_index2
        file_path = file_path1[:end_of_filename + 1] + str(file_index) + "_" + "-1" + file_path1[file_path1.rfind("."):]
        return file_path, file_index

    def retrieve_file_part(self, file_path1, file_path2):
        file_path, file_index = AlgorithmRetrieve.retrieve_file_part_generate_path(file_path1, file_path2)
        if self.part_file_found[file_index]:
            return
        self.part_file[file_index] = file_path
        with open(file_path1, "rb") as f1:
            file1_data = f1.read()
        with open(file_path2, "rb") as f2:
            file2_data = f2.read()
        file_data = file1_data
        for i in range(len(file1_data)):
            file_data[i] ^= file2_data[i]
        with open(file_path, "wb") as f:
            f.write(file_data)
