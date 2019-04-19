import socket
import select

"""
part file name:
filename_part number_if it is a parity file - the other part number, else -1
example:
namg_2_4

"""


class AlgorithmRetrieve():
    def __init__(self, port, num_of_parts):
        #self.server_socket = socket.socket()
        #self.server_socket.bind(('0.0.0.0', port))
        self.open_client_sockets = []
        self.part_file = ["" for i in range(num_of_parts)]  # List[string] - the path of the files
        self.part_file_found = [False for i in range(num_of_parts)]  # List[bool]

    def retrieve_file_part_generate_path(self, file_path1, file_path2):
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
        file_path, file_index = self.retrieve_file_part_generate_path(file_path1, file_path2)
        if self.part_file_found[file_index]:
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
        self.part_file_found[file_index] = True
        self.part_file[file_index] = file_path

    def add_file_path(self, file_path):
        end_of_filename, [file_part_index1, file_part_index2] = get_file_info(file_path)
        if file_part_index2 == -1:
            if not self.part_file_found[file_part_index1]:
                if self.part_file[file_part_index1] != "":
                    self.retrieve_file_part(file_path, self.part_file[file_part_index1])
                else:
                    self.part_file[file_part_index1] = file_path
                    self.part_file_found[file_part_index1] = True
        else:
            if self.part_file_found[file_part_index1] and not self.part_file_found[file_part_index2]:
                self.retrieve_file_part(self.part_file[file_part_index1], file_path)
            elif not self.part_file_found[file_part_index1] and self.part_file_found[file_part_index2]:
                self.retrieve_file_part(self.part_file[file_part_index2], file_path)
            elif not self.part_file_found[file_part_index1] and not self.part_file_found[file_part_index2]:
                self.part_file[file_part_index1] = file_path
                self.part_file[file_part_index2] = file_path

    def is_finish(self):
        return all(self.part_file_found)

    def connect_file(self):
        """
            is_finish() = True
            len(self.part_file) >= 1
        """
        file_part_path = self.part_file[0]
        end_of_filename, [file_part_index1, file_part_index2] = get_file_info(file_part_path)
        file_path = file_part_path[:end_of_filename + 1] + file_part_path[file_part_path.rfind("."):]
        for file_part_path in self.part_file:
            with open(file_part_path,"rb") as fr:
                data = fr.read()
            with open(file_path,"ab") as fw:
                fw.write(data)


def get_file_info(file_path):
    """
    :return: end_of_filename, [file_part_index1,file_part_index2]
    """
    start_of_filename = file_path.rfind("\\") + 1
    end_of_filename = file_path.rfind("_", start_of_filename, file_path.rfind("_"))
    file_part_index1 = int(file_path[end_of_filename + 1: file_path.find("_", end_of_filename + 1)])
    file_part_index2 = int(file_path[file_path.find("_", end_of_filename + 1) + 1: file_path.rfind(".")])
    return end_of_filename, [file_part_index1, file_part_index2]


if __name__ == '__main__':
    get_file_info(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_0_-1.txt")
    a = AlgorithmRetrieve(3,3)
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_-1.txt")
    print a.part_file
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_2.txt")
    print a.part_file
    a.add_file_path(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_0_-1.txt")
    print a.part_file
    a._connect_file()