import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

class ClientCrypto():
    def generate_key(self):
        """
        generate key for RSA
        :return: the key - RSA type
        """
        random_generator = Random.new().read
        key = RSA.generate(1024, random_generator)  # generate pub and priv key
        self.key = key
        self.public_key = key.publickey()


    def __init__(self):
        self.generate_key()

