from Crypto.PublicKey import RSA
from AESCipher import AESCipher
import string
import random
import os


class MainServer_DataServer_Protocol:
    def __init__(self, saving_path):
        """
        constructor
        :param saving_path: to save temp files
        """
        self.saving_path = saving_path
        self.AES_key = ''.join(random.choice(string.digits + string.letters) for _ in range(32))
        self.AES_cipher = AESCipher(self.AES_key)
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            4: self.disassemble_4_get_file}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            3: self.build_3_upload_file,
            4: self.build_4_get_file,
            5: self.build_5_delete_file}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_AES_key(self):
        """
        :return: AES key as string
        """
        return self.AES_key

    def create_RSA_public_key(self, key):
        """
        get RSA key as RSA instance from the key
        :param key:
        :return: RSA instance
        """
        return RSA.importKey(key)

    def recv_msg(self, current_socket, first):
        """
        recv the msg from socket and decrypt it
        :param current_socket: the socket to recv from
        :param first: if it is the first msg-> this is the RSA key
        :return: [msg type - by protocol, msg parameters - [...], connection fails - boolean]
        """
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
        """
        send specific msg to specific socket
        :param current_socket:
        :param msg:
        :return: connection fails boolean
        """
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

    def disassemble_4_get_file(self, msg):
        """
        :param msg: the msg parameters - file part name and data
        :return: msg parameters - in array [file part path (after creating)]
        """
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        msg = msg[msg.find("$") + 1 + name_len:]
        data_len = int(msg[:msg.find("$")])
        data = msg[msg.find("$") + 1: msg.find("$") + 1 + data_len]
        file_part_path = self.saving_path + "\\" + name
        if not os.path.isfile(file_part_path):
            with open(file_part_path, "wb") as f:
                f.write(data)
        return [file_part_path]

    def build(self, msg_type, msg_parameter, RSA_key=None):
        """
        :param RSA_key: if it is the filrst msg and need to encrypt with RSA
        :param msg_type: int - the msg type as above
        :param msg_parameter: array of the parameters
        :return: a string that will be send by the socket to the data server
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

    def build_3_upload_file(self, msg_parameters):
        """
        :param msg_parameters: [file path]
        :return: the msg to send
        """
        name = msg_parameters[0][msg_parameters[0].rfind("\\") + 1:]
        with open(msg_parameters[0], "rb") as f:
            file_data = f.read()
        os.remove(msg_parameters[0])
        msg = str(len(name)) + "$" + name + str(len(file_data)) + "$" + file_data
        return msg

    def build_4_get_file(self, msg_parameters):
        """
        :param msg_parameters: [file name, port]
        :return: the msg to send
        """
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(msg_parameters[1])
        return msg

    def build_5_delete_file(self, msg_parameters):
        """
        :param msg_parameters: [file name]
        :return: the msg to send
        """
        msg = msg_parameters[0]
        return msg
