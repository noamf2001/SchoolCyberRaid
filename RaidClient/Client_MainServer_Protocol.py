from Crypto.PublicKey import RSA
from Crypto import Random
from AESCipher import AESCipher
import gzip
import shutil
import hashlib

class Client_MainServer_Protocol():
    def __init__(self, my_socket, saving_path):
        self.saving_path = saving_path
        random_generator = Random.new().read
        self.RSA_key = RSA.generate(1024, random_generator)  # generate pub and priv key
        self.AES_cipher = None
        self.my_socket = my_socket
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            1: self.disassemble_1_sign_up,
            2: self.disassemble_2_sign_in,
            3: self.disassemble_3_upload_file,
            4: self.disassemble_4_get_file,
            6: self.disassemble_6_get_file_list}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            1: self.build_1_sign_up,
            2: self.build_2_sign_in,
            3: self.build_3_upload_file,
            4: self.build_4_get_file,
            5: self.build_5_delete_file,
            6: self.build_6_get_file_list}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_RSA_public_key(self):
        return self.RSA_key.publickey().exportKey()

    def create_AES_key(self, password):
        print "create AESCipher"
        self.AES_cipher = AESCipher(password)

    def recv_msg(self, first=False):
        connection_fail = False
        # recv the msg length
        msg_len = ""
        try:
            msg_len = self.my_socket.recv(1)
        except:
            return -1, [], True
        while msg_len[-1] != "$":
            try:
                msg_len += self.my_socket.recv(1)
            except:
                return -1, [], True
        msg_len = int(msg_len[:-1])
        msg = ""
        try:
            msg = self.my_socket.recv(msg_len)
        except:
            return -1, [], True

        msg_type, msg_parameters = self.disassemble(msg, first)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, msg):
        connection_fail = False
        try:
            self.my_socket.send(msg)
        except:
            connection_fail = True
        return connection_fail

    def get_msg_type(self, msg):
        """
        :param msg: the raw full msg - string (without the len of the msg) (len > 0)
        :return: msg type - int, msg msg without the msg_type part
        """
        end_of_msg_type = msg.find("$")
        msg_type = int(msg[:end_of_msg_type])
        msg = msg[end_of_msg_type + 1:]
        return msg_type, msg

    def disassemble(self, msg, first):
        """
        :param first: if it is the first msg from MainServer
        :param msg: the raw full msg - string (without the len of the msg) (len > 0)
        :return: msg type - int, msg parameters - array []
        """
        if first:
            msg = self.RSA_key.decrypt(msg)
        else:
            msg = self.AES_cipher.decrypt(msg)
        msg_type, msg = self.get_msg_type(msg)
        msg_parameters = self.msg_type_disassemble[msg_type](msg)
        if msg_type == 4:
            print "???"
        return msg_type, msg_parameters

    def disassemble_0_key_exchange(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array []
        """
        return [msg]

    def disassemble_1_sign_up(self, msg):
        """
        :param msg: the msg parameters - boolean: 0 - False, 1 - True
        :return: msg parameters - in array []
        """
        return [bool(int(msg))]

    def disassemble_2_sign_in(self, msg):
        """
        :param msg: the msg parameters - boolean: 0 - False, 1 - True
        :return: msg parameters - in array []
        """
        return [bool(int(msg))]

    def disassemble_3_upload_file(self, msg):
        """
        :param msg: the msg parameters - boolean: 0 - False, 1 - True
        :return: msg parameters - in array []
        """
        return [bool(int(msg))]

    def decompress_file(self, file_path):
        file_path_new = file_path[:file_path.rfind("_")] + "." + file_path[
                                                                 file_path.rfind("_") + 1:file_path.rfind(".")]
        with gzip.open(file_path, 'rb') as f_in:
            with open(file_path_new, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return file_path_new

    def disassemble_4_get_file(self, msg):
        """
        :param msg: the msg parameters - file part name and data
        :return: msg parameters - in array [file part path (after creating)]
        """
        print "disassemble 4 get file???!!!!"
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        msg = msg[msg.find("$") + 1 + name_len:]
        data_len = int(msg[:msg.find("$")])
        if data_len != 0:
            data = msg[msg.find("$") + 1: msg.find("$") + 1 + data_len]
            file_path = self.saving_path + "\\" + name
            print "save in file part path: " + file_path
            # while os.path.isfile(file_part_path):
            #    file_part_path = file_part_path[:file_part_path.rfind(".")] + str(random.randint(0, 100)) + file_part_path[
            #                                                                                                file_part_path.rfind("."):]
            with open(file_path, "wb") as f:
                f.write(data)
        else:
            file_path = ""
            print "data is \"\""
        if file_path != "":
            file_path = self.decompress_file(file_path)
        return [file_path]

    def disassemble_6_get_file_list(self, msg):
        """
        :param msg: the msg parameters all the files
        :return: msg parameters - in array [file 1 name,....,]
        """
        print "disassemble_6_get_file_list: " + msg
        current_index = 0
        result_file = []

        while current_index < len(msg):
            print current_index
            name_len = int(msg[current_index:msg.find(r"$", current_index)])
            name = msg[msg.find(r"$", current_index) + 1: msg.find(r"$", current_index) + 1 + name_len]
            result_file.append(name)
            current_index = msg.find(r"$", current_index) + name_len + 1
        return result_file

    def build(self, msg_type, msg_parameter):
        """
        :param msg_type: int - the msg type as above
        :param msg_parameter: array of the parameters
        :return: a string that will be send by the socket to the client
        """
        print "build the msg with msg type: " + str(msg_type)
        msg = str(msg_type) + "$" + self.msg_type_build[msg_type](msg_parameter)
        if msg_type != 0:
            encrypted_msg = self.AES_cipher.encrypt(msg)
        else:
            encrypted_msg = msg
        encrypted_msg = str(len(encrypted_msg)) + "$" + encrypted_msg
        return encrypted_msg

    def build_0_key_exchange(self, msg_parameters):
        """
        :param msg_parameters: [key]
        :return: key
        """
        return msg_parameters[0]

    def hash_password(self, password):
        """
        :param password: string
        :return: str of length 64 - the hash
        """
        return password
        # return hashlib.sha256(password).hexdigest()

    def build_1_sign_up(self, msg_parameters):
        """
        :param msg_parameters: [username, password (after hash)]
        :return: the msg to send
        """
        hash_password = self.hash_password(msg_parameters[1])
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(len(hash_password )) + "$" + \
              hash_password
        return msg

    def build_2_sign_in(self, msg_parameters):
        """
        :param msg_parameters: [username, password (after hash)]
        :return: the msg to send
        """
        hash_password = self.hash_password(msg_parameters[1])
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(len(hash_password)) + "$" + \
              hash_password[1]
        return msg

    def compress_file(self, file_name, file_path):
        file_name_new = file_name[:file_name.rfind(".")] + "_" + file_name[file_name.rfind(".") + 1:] + '.gz'
        f_in = open(file_path)
        f_out = gzip.open(file_name_new, 'wb')
        f_out.writelines(f_in)
        f_out.close()
        f_in.close()
        return file_name_new

    def build_3_upload_file(self, msg_parameters):
        """
        :param msg_parameters: [file name, file path]
        :return: the msg to send
        """
        file_name = self.compress_file(msg_parameters[0], msg_parameters[1])
        with open(file_name, "rb") as f:
            file_data = f.read()
        msg = str(len(file_name)) + "$" + file_name + str(len(file_data)) + "$" + file_data
        return msg

    def build_4_get_file(self, msg_parameters):
        """
        :param msg_parameters: [file name]
        :return: the msg to send
        """
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0]
        return msg

    def build_5_delete_file(self, msg_parameters):
        """
        :param msg_parameters: [file name]
        :return: the msg to send
        """
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0]
        return msg

    def build_6_get_file_list(self, msg_parameters):
        """
        :param msg_parameters: [""]
        :return: the msg to send
        """
        return ""


if __name__ == '__main__':
    a = Client_MainServer_Protocol("sock")
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
