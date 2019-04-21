import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
from AESCipher import AESCipher
import ast
from Crypto.Cipher import AES
import hashlib
"""
msg:
len of msg
$
msg type
$
msg parameters

msg parameters is organize by msg type

msg type:
0:  key exchange,
        client to server: asymmetric key
        server to client: symmetric key
    msg parameters:
        just the key itself
"""


class Client_MainServer_Protocol():
    def __init__(self, my_socket):
        random_generator = Random.new().read
        self.RSA_key = RSA.generate(1024, random_generator)  # generate pub and priv key
        print "RSA_key: " + self.export_RSA_public_key()
        self.AES_cipher = None
        self.encrypter = None
        self.decrypter = None
        self.my_socket = my_socket
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_RSA_public_key(self):
        return self.RSA_key.publickey().exportKey()

    def create_AES_key(self, password):
        self.AES_cipher = AESCipher(password)

    def recv_msg(self, first = False):
        connection_fail = False
        # recv the msg length
        msg_len = ""
        try:
            msg_len = self.my_socket.recv(1)
        except:
            connection_fail = True
        while msg_len[-1] != "$":
            try:
                msg_len += self.my_socket.recv(1)
            except:
                connection_fail = True
        msg_len = int(msg_len[:-1])
        msg = ""
        try:
            msg = self.my_socket.recv(msg_len)
        except:
            connection_fail = True
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
        print "disassemble: " + msg
        if first:
            msg = self.RSA_key.decrypt(msg)
        else:
            msg = self.AES_cipher.decrypt(msg)
        msg_type, msg = self.get_msg_type(msg)
        msg_parameters = self.msg_type_disassemble[msg_type](msg)
        return msg_type, msg_parameters

    def disassemble_0_key_exchange(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array []
        """
        return [msg]

    def build(self, msg_type, msg_parameter):
        """
        :param msg_type: int - the msg type as above
        :param msg_parameter: array of the parameters
        :return: a string that will be send by the socket to the client
        """
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


if __name__ == '__main__':
    a = Client_MainServer_Protocol("sock")
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
