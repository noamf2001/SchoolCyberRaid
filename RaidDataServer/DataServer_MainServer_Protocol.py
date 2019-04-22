from Crypto.PublicKey import RSA
from Crypto import Random
from AESCipher import AESCipher

"""
msg:
len of msg
$
msg type
$
msg parameters

msg parameters is organize by msg type

msg type:
-1: socket crash
0:  key exchange,
        data server to server: asymmetric key
        server to data server: symmetric key
    msg parameters:
        just the key itself
"""


class DataServer_MainServer_Protocol():
    def __init__(self, my_socket):
        random_generator = Random.new().read
        self.RSA_key = RSA.generate(1024, random_generator)  # generate pub and priv key
        self.AES_cipher = None
        self.encrypter = None
        self.decrypter = None
        self.my_socket = my_socket
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            1: self.disassemble_1_sign_up,
            2: self.disassemble_2_sign_in}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            1: self.build_1_sign_up,
            2: self.build_2_sign_in}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_RSA_public_key(self):
        return self.RSA_key.publickey().exportKey()

    def create_AES_key(self, password):
        print "create AESCipher"
        self.AES_cipher = AESCipher(password)

    def recv_msg(self, first=False):
        print "continue start recv msg 1"
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

        print "continue start recv msg 2"
        msg_type, msg_parameters = self.disassemble(msg, first)

        print "continue start recv msg 3"
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

    def build(self, msg_type, msg_parameter):
        """
        :param msg_type: int - the msg type as above
        :param msg_parameter: array of the parameters
        :return: a string that will be send by the socket to the main server
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

    def build_1_sign_up(self, msg_parameters):
        """
        :param msg_parameters: [username, password (after hash)]
        :return: the msg to send
        """
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(len(msg_parameters[1])) + "$" + \
              msg_parameters[1]
        return msg

    def build_2_sign_in(self, msg_parameters):
        """
        :param msg_parameters: [username, password (after hash)]
        :return: the msg to send
        """
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(len(msg_parameters[1])) + "$" + \
              msg_parameters[1]
        return msg

    def build_3_upload_file(self, msg_parameters):
        """
        :param msg_parameters: [file name, file path]
        :return: the msg to send
        """
        with open(msg_parameters[1], "rb") as f:
            file_data = f.read()
        msg = str(len(msg_parameters[0])) + "$" + msg_parameters[0] + str(len(file_data)) + "$" + file_data
        return msg


if __name__ == '__main__':
    a = DataServer_MainServer_Protocol("sock")
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
