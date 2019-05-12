from Crypto.Cipher import AES
import hashlib
from Crypto.PublicKey import RSA
from Crypto import Random
from AESCipher import AESCipher
import string
import random
import os



class MainServer_Client_Protocol():
    def __init__(self, saving_path):
        self.AES_key = ''.join(random.choice(string.digits + string.letters) for _ in range(32))
        self.saving_path = saving_path
        self.AES_cipher = AESCipher(self.AES_key)
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            1: self.disassemble_1_sign_up,
            2: self.disassemble_2_sign_in,
            3: self.disassemble_3_upload_file,
            4: self.disassemble_4_get_file,
            5: self.disassemble_5_delete_file,
            6: self.disassemble_6_get_file_list}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            1: self.build_1_sign_up,
            2: self.build_2_sign_in,
            3: self.build_3_upload_file,
            4: self.build_4_get_file,
            6: self.build_6_get_file_list}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_AES_key(self):
        return self.AES_key

    def create_RSA_public_key(self, key):
        return RSA.importKey(key)

    def recv_msg(self, current_socket, first):
        # recv the msg length
        try:
            msg_len = current_socket.recv(1)
        except:
            return -1, [], True
        while msg_len[-1] != "$":
            try:
                msg_len += current_socket.recv(1)
            except:
                return -1, [], True
        msg_len = int(msg_len[:-1])
        try:
            msg = current_socket.recv(msg_len)
        except:
            return -1, [], True
        msg_type, msg_parameters = self.disassemble(msg, first)
        return msg_type, msg_parameters, False

    def send_msg(self, current_socket, msg):
        connection_fail = False
        try:
            current_socket.send(msg)
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
        :param first: if this is the first msg -> the public RSA key
        :param msg: the raw full msg - string (without the len of the msg) (len > 0) (encrypted)
        :return: msg type - int, msg parameters - array []
        """
        if not first:
            msg = self.AES_cipher.decrypt(msg)
        msg_type, msg = self.get_msg_type(msg)
        msg_parameters = self.msg_type_disassemble[msg_type](msg)
        return msg_type, msg_parameters

    def disassemble_0_key_exchange(self, msg):
        """
        :param msg: the msg parameters - key
        :return: msg parameters - in array []
        """
        return [msg]

    def disassemble_username_password(self, msg):
        """
        :param msg: the msg parameters - username and password
        :return: the msg parameters in array [username, password]
        """
        username_start = msg.find("$")
        username_len = int(msg[:username_start])
        username = msg[username_start + 1:username_start + 1 + username_len]
        password_start = msg.find("$", username_start + 1 + username_len)
        password_len = int(msg[username_start + 1 + username_len: password_start])
        password = msg[password_start + 1:password_start + 1 + password_len]
        return [username, password]

    def disassemble_1_sign_up(self, msg):
        """
        :param msg: the msg parameters
        :return: the msg parameters in array [username, password]
        """
        return self.disassemble_username_password(msg)

    def disassemble_2_sign_in(self, msg):
        """
        :param msg: the msg parameters
        :return: the msg parameters in array [username, password]
        """
        return self.disassemble_username_password(msg)

    def disassemble_3_upload_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [path]
        """
        print "disassemble_3_upload_file"
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        msg = msg[msg.find("$") + 1 + name_len:]
        data_len = int(msg[:msg.find("$")])
        data = msg[msg.find("$") + 1: msg.find("$") + 1 + data_len]
        file_part_path = self.saving_path + "\\" + name
        print "files part path:" + file_part_path
        print data_len
        # while os.path.isfile(file_part_path):
        #    file_part_path = file_part_path[:file_part_path.rfind(".")] + str(random.randint(0, 100)) + file_part_path[
        #                                                                                                file_part_path.rfind("."):]
        #if os.path.isfile(file_part_path):
        #    os.remove(file_part_path)
        if data_len == 0:
            f = open(file_part_path,"wb")
            f.close()
        with open(file_part_path, "wb") as f:
            f.write(data)
        return [file_part_path]

    def disassemble_4_get_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [file_name]
        """
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        return [name]

    def disassemble_5_delete_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [file_name]
        """
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        return [name]

    def disassemble_6_get_file_list(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array []
        """
        return []

    def build(self, msg_type, msg_parameter, RSA_key=None):
        """
        :param RSA_key: if it is the filrst msg and need to encrypt with RSA
        :param msg_type: int - the msg type as above
        :param msg_parameter: array of the parameters
        :return: a string that will be send by the socket to the client
        """
        msg = str(msg_type) + "$" + self.msg_type_build[msg_type](msg_parameter)
        if RSA_key is not None:
            encrypted_msg = RSA.importKey(RSA_key).encrypt(msg, "x")[0]
        else:
            encrypted_msg = self.AES_cipher.encrypt(msg)
        encrypted_msg = str(len(encrypted_msg)) + "$" + encrypted_msg
        return encrypted_msg

    def build_0_key_exchange(self, msg_parameters):
        """
        :param msg_parameters: [AES_key]
        :return: key
        """
        return msg_parameters[0]

    def build_1_sign_up(self, msg_parameters):
        """
        :param msg_parameters: [boolean]
        :return: 1 if True, 0 if False
        """
        return str(int(msg_parameters[0]))

    def build_2_sign_in(self, msg_parameters):
        """
        :param msg_parameters: [boolean]
        :return: 1 if True, 0 if False
        """
        return str(int(msg_parameters[0]))

    def build_3_upload_file(self, msg_parameters):
        """
        :param msg_parameters: [file_name,boolean]
        :return: file name + 1 if True, 0 if False
        """
        file_name = msg_parameters[0][msg_parameters[0].rfind("$") + 1:]
        msg = str(len(file_name)) + "$" + file_name + str(int(msg_parameters[1]))
        return msg

    def build_4_get_file(self, msg_parameters):
        """
        :param msg_parameters: [file_name,file_path]
        :return: file name and file data
        """
        file_name = msg_parameters[0][msg_parameters[0].rfind("$") + 1:]
        if msg_parameters[1] != "":
            with open(msg_parameters[1], "rb") as f:
                file_data = f.read()
            os.remove(msg_parameters[1])
        else:
            file_data = ""
        msg = str(len(file_name)) + "$" + file_name + str(len(file_data)) + "$" + file_data
        return msg

    def build_6_get_file_list(self,msg_parameters):
        """
        :param msg_parameters: [file 1 name, file 2 name,...]
        :return: the msg combiend it lie always
        """
        msg = ""
        for file_name in msg_parameters:
            msg += str(len(file_name)) + "$" + file_name
        return msg


if __name__ == '__main__':
    a = MainServer_Client_Protocol()
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
