import os

"""
part file name:
filename_part number_if it is a parity file - the other part number, else -1
"""

PART_FILE_LENGTH = 5


def create_parity_file_part_path(file_path1, file_path2):
    end_of_filename1, [file_part1_index1, file_part1_index2] = get_file_info(file_path1)
    end_of_filename2, [file_part2_index1, file_part2_index2] = get_file_info(file_path2)
    parity_file_path = file_path1[:end_of_filename1 + 1] + str(min(file_part1_index1, file_part2_index1)) + "_" + str(
        max(file_part1_index1, file_part2_index1)) + file_path1[file_path1.rfind("."):]
    return parity_file_path


def create_parity_file_part(file_path1, file_path2):
    """
    create the parity file out of there two.
    the files have the same length
    :param file_path1: the name is built as mention above
    :param file_path2: the name is built as mention above
    :return path to the parity file
            None if something wrong with those file
            save the file in file1 path
    """
    parity_file_path = create_parity_file_part_path(file_path1, file_path2)

    with open(file_path1, "rb") as file1:
        file_data1 = bytearray(file1.read())
    with open(file_path2, "rb") as file2:
        file_data2 = bytearray(file2.read())
    parity_file_data = bytearray(len(file_data1))
    for i in range(len(file_data1)):
        parity_file_data[i] = file_data1[i] ^ file_data2[i]
    with open(parity_file_path, "wb") as parity_file:
        parity_file.write(parity_file_data)


def create_parity_files(file_path):
    """
    :param file_path: the path of the file to save
    :return [parts_num, file_len,[file_part - 1 - path,....]
    """
    parts = split_file(file_path)
    file_len = os.path.getsize(file_path)
    file_part_path = []
    for i in range(len(parts) - 1):
        file_part_path.append(create_parity_file_part(parts[i], parts[i + 1]))
    return parts,file_len, file_part_path


def split_file(file_path):
    """
    split to file to part file with the same length as PART_FILE_LENGTH
    complete the part file that(if exists) is not at that length with 0 (the ascii char with ascii value 0)
    save the parts file as expected as above
    :param file_path: the path of the file to split
    :return: the number of file parts created
    """
    parts = []
    parts_num = os.path.getsize(file_path) / PART_FILE_LENGTH

    if os.path.getsize(file_path) % PART_FILE_LENGTH != 0:
        parts_num += 1
    with open(file_path, "rb") as file:
        for i in range(parts_num):
            file_part_data = file.read(PART_FILE_LENGTH)
            file_part_name = file_path[:file_path.rfind(".")] + "_" + str(i) + "_" + "-1" + file_path[
                                                                                            file_path.rfind("."):]
            parts.append(file_part_name)
            with open(file_part_name, "wb") as file_part:
                file_part.write(file_part_data)
                if len(file_part_data) < PART_FILE_LENGTH:
                    file_part.write(chr(0))
    return parts


def divide_parts_to_ds(files_part_path, data_servers):
    """
    need better algorithm
    Get from DB the ds current storage state and decide how to put the parts in the ds
    :param files_part_path: [file part path1,....]
    :param data_servers: [(data_server_1,),....]
    :return [[data_server_1,[file_part,...]],[data_server2,[file_part,...]]....]
    """
    result = [[data_server, []] for data_server in data_servers]
    for i in range(len(files_part_path)):
        result[i % len(data_servers)][1].append(files_part_path[i])
    return result



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
    split_file(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename.txt")
    create_parity_file_part(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_2_-1.txt",
                            r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_-1.txt")
