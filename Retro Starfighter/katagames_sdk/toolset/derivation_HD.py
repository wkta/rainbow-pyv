
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import scrypt
#from Crypto.Random import get_random_bytes
import random
from Crypto.PublicKey import RSA
from Crypto.Hash import HMAC
from struct import pack


def get_random_bytes(e_len):
    rb = [ random.randint(0,255) for _ in range(e_len) ]
    return bytes(rb)


def generate_precursor(hexa_repr, idx: int):
    if hexa_repr[0] == '0' and hexa_repr[1] == 'x':
        hexa_repr = hexa_repr[2:]
    
    big_int = int(hexa_repr, 16)
    random.seed(big_int)

    pwd = b'laditegaietaliebl897'
    salt = get_random_bytes(24)

    key = scrypt(pwd, salt, 32, N=2**4, r=8, p=idx)  # N was 2**14
    return key, key.hex()


# --------------------

def gen_rsa_kp(precursor_b):
    # The first key could also be read from a file
    first_key = RSA.importKey(b'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6WFHGQItFVNGMqNwkW0d6tSp0i250s3JmMO8yCV1IKQ4yKIh8lhZPzlAuHmzeLO2kUvqq+WYKeQfJ08JM9lC39qIiYUZBv9NMTnsiwRXd1v3NNwb4DTw28hhAVmf8V84WFvK/ctPXE5iOeEKwCIW3CSDan+vt+Vv0PIH0OF73Jkdj8hDkfPiCIwB5YVEPD2l0lpzva7n33tveEXQDGvl2yPmEHQkJGdGJkHbRZ0t2E3jmKVctdlrP4qYUjREoEX9YT5yAs8wEXjK6UqNWgTQsX+/YPvqA8sqH6XvnMHQyh960DvXp45E19xVUxZG7xt2/5oJtrJ1bV6v51laN5GUx')
     # RSA.generate(2048)

    # Here we encode the first key into bytes and in a platform-independent format.
    # The actual format is not important (PKCS#1 in this case), but it must
    # include the private key.
    encoded_first_key = first_key.exportKey('DER')

    seed_128 = HMAC.new(encoded_first_key + precursor_b).digest()

    class PRNG(object):
      def __init__(self, seed):
        self.index = 0
        self.seed = seed
        self.buffer = b""

      def __call__(self, n):
        while len(self.buffer) < n:
            self.buffer += HMAC.new(self.seed +
                                    pack("<I", self.index)).digest()
            self.index += 1
        result, self.buffer = self.buffer[:n], self.buffer[n:]
        return result

    res_pr_k = RSA.generate(2048, randfunc=PRNG(seed_128))
    return res_pr_k
    # print(second_keyp.exportKey('OpenSSH'))

from test_RSA import crypt, decrypt

##gen_rsa_kp(btab[0])
##print()
##gen_rsa_kp(btab[1])

