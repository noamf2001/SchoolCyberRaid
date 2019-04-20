from Crypto.Cipher import AES
import hashlib

import string
import random
"""
msg type:
0: key exchange,
    client to server: asymmetric key
    server to client: symmetric key
"""


class MainServer_Client_Protocol():
    def __init__(self):
        password = ''.join(random.choice(string.digits + string.letters) for _ in range(32))
        self.AES_key = hashlib.sha256(password).digest()
        IV = 16 * '\x00'  # Initialization vector: discussed later
        mode = AES.MODE_CBC
        self.encrypter = AES.new(self.AES_key, mode, IV=IV)
        self.decrypter = AES.new(self.AES_key, mode, IV=IV)
        self.RSA_key = None

    def recv_msg(self, current_socket):
        connection_fail = False
        # recv the msg length
        msg_len = ""
        try:
            msg_len = current_socket.recv(1)
        except:
            connection_fail = True
        while msg_len[-1] != "$":
            try:
                msg_len += current_socket.recv(1)
            except:
                connection_fail = True
        msg_len = int(msg_len[:-1])
        msg = ""
        try:
            msg = current_socket.recv(msg_len)
        except:
            connection_fail = True
        msg_type, msg_parameters = self.disassemble(msg)
        return msg_type, msg_parameters, connection_fail

    def send_msg(self, current_socket, msg):
        connection_fail = False
        try:
            current_socket.send(msg)
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
