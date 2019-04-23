from Crypto.Cipher import AES
import hashlib
from Crypto.PublicKey import RSA
from Crypto import Random
from AESCipher import AESCipher
import string
import random
import os

"""
msg type:
-1: socket crash
0: key exchange,
    client to server: asymmetric key
    server to client: symmetric key
    msg parameters:
        just the key itself
1:  sign up:
        client to server: username, password (after hash)
        server to client: boolean if success
    msg parameters:
        len of username
        $
        username
        
        len of password
        $
        password
2:  sign in:
        client to server: username, password(after hash)
        server to client: boolean if success
    msg parameters:
        client to server: 
            len of username
            $
            username
            
            len of password
            $
            password
        server to client:
            0 - False
            1 - True
3:  upload file:
        client to server: file name, file data
        server to client: boolean if success
    msg parameters:
        client to server:
            len of file
            $
            file name
            
            len of file data
            $
            file data
        server to client:
            0 - False
            1 - True
"""


class MainServer_Client_Protocol():
    def __init__(self, saving_path):
        self.AES_key = ''.join(random.choice(string.digits + string.letters) for _ in range(32))
        self.saving_path = saving_path
        self.AES_cipher = AESCipher(self.AES_key)
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            1: self.disassemble_1_sign_up,
            2: self.disassemble_2_sign_in}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            1: self.build_1_sign_up,
            2: self.build_2_sign_in,
            3: self.build_3_upload_file}  # msg type (int) : method that build the msg to send, the msg parameters part

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
        print "disassemble sign up/in:  " + str([username, password])
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
        :return: msg parameters - in array []
        """
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        msg = msg[msg.find("$") + 1 + name_len:]
        data_len = int(msg[:msg.find("$")])
        data = msg[msg.find("$") + 1: msg.find("$") + 1 + data_len]
        file_part_path = self.saving_path + "\\" + name
        while os.path.isfile(file_part_path):
            file_part_path = file_part_path[:file_part_path.rfind(".")] + str(random.randint(0, 100)) + file_part_path[
                                                                                                        file_part_path.rfind(
                                                                                                            "."):]
        with open(file_part_path, "wb") as f:
            f.write(data)
        return [name, file_part_path]

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
        :param msg_parameters: [boolean]
        :return: 1 if True, 0 if False
        """
        return str(int(msg_parameters[0]))


if __name__ == '__main__':
    a = MainServer_Client_Protocol()
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
