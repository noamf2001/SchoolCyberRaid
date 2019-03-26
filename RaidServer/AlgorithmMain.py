import os

"""
part file name:
filename_partnumber_if it is a parity file - the other part number, else -1
"""

PART_FILE_LENGTH = 5


def create_parity_file_part_path(file_path1, file_path2):
    start_of_filename = file_path1.rfind("\\") + 1
    end_of_filename = file_path1.rfind("_", start_of_filename, file_path1.rfind("_"))
    file_part1_index = int(file_path1[end_of_filename + 1: file_path1.find("_", end_of_filename + 1)])
    file_part2_index = int(file_path2[end_of_filename + 1: file_path2.find("_", end_of_filename + 1)])
    parity_file_path = file_path1[:end_of_filename + 1] + str(min(file_part1_index, file_part2_index)) + "_" + \
                       str(max(file_part1_index, file_part2_index)) + file_path1[file_path1.rfind("."):]
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


def split_file(file_path):
    """
    split to file to part file with the same length as PART_FILE_LENGTH
    complete the part file that(if exists) is not at that length with 0 (the ascii char with ascii value 0)
    save the parts file as expected as above
    :param file_path: the path of the file to split
    :return: the number of file parts created
    """
    with open(file_path, "rb") as file:
        parts_num = os.path.getsize(file_path) / PART_FILE_LENGTH
        if len(file_path) % PART_FILE_LENGTH != 0:
            parts_num += 1
        for i in range(parts_num):
            file_part_data = file.read(PART_FILE_LENGTH)
            file_part_name = file_path[:file_path.rfind(".")] + "_" + str(i) + "_" + "-1" + file_path[
                                                                                            file_path.rfind("."):]
            with open(file_part_name, "wb") as file_part:
                file_part.write(file_part_data)
                print len(file_part_data)
                if len(file_part_data) < PART_FILE_LENGTH:
                    file_part.write(chr(0))
        return parts_num

if __name__ == '__main__':
    split_file(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename.txt")
    create_parity_file_part(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_2_-1.txt",
                            r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_1_-1.txt")