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
3: upload file,
    main server to data server: file name, file data
    data server to main server: None
    msg parameters:
        file name
        file data
"""


class DataServer_MainServer_Protocol():
    def __init__(self, my_socket, saving_path):
        self.saving_path = saving_path
        random_generator = Random.new().read
        self.RSA_key = RSA.generate(1024, random_generator)  # generate pub and priv key
        self.AES_cipher = None
        self.my_socket = my_socket
        self.msg_type_disassemble = {
            0: self.disassemble_0_key_exchange,
            3: self.disassemble_3_upload_file,
            4: self.disassemble_4_get_file,
            5: self.disassemble_5_delete_file}  # msg type (int) : method that disassemble the msg parameters
        self.msg_type_build = {
            0: self.build_0_key_exchange,
            4: self.build_4_get_file}  # msg type (int) : method that build the msg to send, the msg parameters part

    def export_RSA_public_key(self):
        return self.RSA_key.publickey().exportKey()

    def create_AES_key(self, password):
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
        return msg_type, msg_parameters

    def disassemble_0_key_exchange(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array []
        """
        return [msg]

    def disassemble_3_upload_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [file part path]
        """
        # print "last: " + msg
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        msg = msg[msg.find("$") + 1 + name_len:]
        data_len = int(msg[:msg.find("$")])
        data = msg[msg.find("$") + 1: msg.find("$") + 1 + data_len]
        file_part_path = self.saving_path + "\\" + name
        with open(file_part_path, "wb") as f:
            f.write(data)
        return [file_part_path]

    def disassemble_4_get_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [file_name, port]
        """
        print "print disassemble get file: " + msg
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        port = int(msg[msg.find("$") + 1 + name_len:])
        return [name, port]

    def disassemble_5_delete_file(self, msg):
        """
        :param msg: the msg parameters
        :return: msg parameters - in array [file_name]
        """
        print "print disassemble get file: " + msg
        name_len = int(msg[:msg.find("$")])
        name = msg[msg.find("$") + 1: msg.find("$") + 1 + name_len]
        return [name]
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

    def build_4_get_file(self, msg_parameters):
        """
        :param msg_parameters: [file_name,file_path]
        :return: file name and file data
        """

        file_name = msg_parameters[0]
        if msg_parameters[1] != "":
            with open(msg_parameters[1], "rb") as f:
                file_data = f.read()
        else:
            file_data = ""
        msg = str(len(file_name)) + "$" + file_name + str(len(file_data)) + "$" + file_data
        return msg


if __name__ == '__main__':
    a = DataServer_MainServer_Protocol("sock")
    b = a.build(0, ["noamfluss"])
    print b
    print a.disassemble(b[b.find("$") + 1:])
