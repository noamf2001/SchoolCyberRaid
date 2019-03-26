"""
part file name:
filename_partnumber_if it is a parity file - the other part number, else -1
"""


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
    :param file_path1:
    :param file_path2:
    :return path to the parity file
            None if something wrong with those file
            save the file in file1 path
    """
    parity_file_path = create_parity_file_part_path(file_path1,file_path2)

    with open(file_path1, "rb") as file1:
        file_data1 = bytearray(file1.read())
    with open(file_path2, "rb") as file2:
        file_data2 = bytearray(file2.read())
    parity_file_data = bytearray(max(len(file_data1),len(file_data2)))
    for i in range(min(len(file_data1),len(file_data2))):
        parity_file_data[i] = file_data1[i] ^ file_data2[i]
        print str(file_data1[i]) + "\t" + str(file_data2[i]) + "\t" + str(parity_file_data[i])
    for i in range(min(len(file_data1),len(file_data2)), max(len(file_data1),len(file_data2))):
        if len(file_data1) > len(file_data2):
            parity_file_data[i] = file_data1[i]
        else:
            parity_file_data[i] = file_data2[i]
    with open(parity_file_path, "wb") as parity_file:
        parity_file.write(parity_file_data)

if __name__ == '__main__':
    create_parity_file_part(r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_13_142.txt",
                                 r"C:\Users\Sharon\Documents\school\cyber\Project\try\somename_142_-1.txt")
