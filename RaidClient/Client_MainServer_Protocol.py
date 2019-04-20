import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

"""
msg type:
0: key exchange,
    client to server: asymmetric key
    server to client: symmetric key
"""


class Client_MainServer_Protocol():
    def __init__(self, my_socket):
        random_generator = Random.new().read
        self.RSA_key = RSA.generate(1024, random_generator)  # generate pub and priv key
        self.AES_key = None
        self.my_socket = my_socket

    def export_RSA_public_key(self):
        return self.RSA_key.publickey().exportKey('DER')

    def recv_msg(self):
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
        msg_type, msg_parameters = self.disassemble(msg)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, msg):
        connection_fail = False
        try:
            self.my_socket.send(msg)
        except:
            connection_fail = True
        return connection_fail

    def disassemble(self, msg):
        """
        :param msg: the raw full msg - string
        :return: msg type - int, msg parameters - array []
        """
        return 0, []

    def build(self, msg_type, parameter):
        """
        :param msg_type: int - the msg type as above
        :param parameter: array of the parameters
        :return: a string that will be send by the socket to the client
        """
        return ""
