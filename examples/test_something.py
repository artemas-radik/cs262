#RANDOM DUMP

import unittest
import random
import string
import sys
from enum import Enum

class Payload(Enum):
    register = 0
    login = 1
    deleteacc = 2
    accdump = 3
    accfilter = 4
    message = 5
    error = 6
    success = 7
    newmessage = 8
 

def decode(buffer):
    match buffer[0]:
        case Payload.error.value:
            return f"[WARNING] {buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}"
        case Payload.success.value:
            return f"[SUCCESS] {buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}"
        case Payload.newmessage.value:
            return f"[MESSAGE] <{buffer[3:int.from_bytes(buffer[1:3],'big')+3].decode('ascii')}> {buffer[int.from_bytes(buffer[1:3],'big')+3:]}"
        case _:
            sys.exit(f"[FAILURE] Undecodable transfer buffer received.")


def encode(command):
    elements = command.split(' ')
    # TODO: Check fields to make sure they fit in types.
    match elements[0]:
        case Payload.register.name:
            return Payload.register.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case Payload.login.name:
            return Payload.login.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case Payload.deleteacc.name:
            return Payload.deleteacc.value.to_bytes(1, 'big')
        case Payload.accdump.name:
            return Payload.accdump.value.to_bytes(1, 'big')
        case Payload.accfilter.name:
            return Payload.accfilter.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii')
        case Payload.message.name:
            return Payload.login.value.to_bytes(1, 'big') + len(elements[1]).to_bytes(2, 'big') + elements[1].encode('ascii') + len(elements[2]).to_bytes(2, 'big') + elements[2].encode('ascii')
        case _:
            print("[FAILURE] Incorrect command usage.")


def randomized_commands(n, m, fname):
    letters = string.ascii_lowercase #thanks https://pynative.com/python-generate-random-string/
    letters += '.^$*+?\{\}[]\\|()'
    args = []

    for i in range(2):
        sub_str = ''.join(random.choice(letters) for j in range(m))
        args.append(sub_str)

    lst = [""]*n
    for i in range(n):
        x = int(random.random() * len(Payload))
        y = int(random.random() * len(Payload))
        s = Payload(x).name
        lst[i] = f"{s} {' '.join(sub_str+str(y) for sub_str in args)}"
    
    with open(fname, 'w') as fp: #thanks https://pynative.com/python-write-list-to-file/
        for comm in lst:
            fp.write("%s\n" % comm)

#randomized_commands(100, 8, 'commands_lst.txt')

class TestClient(unittest.TestCase):
    def test_encode(self):
        self.assertEqual(1, 1)
    
    def test_decode(self):
        self.assertEqual(1, 1)
    
    def inverse(self):
        fname = "commands_lst.txt"
        with open(fname, 'r') as fp:
            comm = fp.readline().strip('\n')
            print(comm)
            print(encode(comm))
            assert(decode(encode(comm)) == comm), "decode(encode(x)) != x"

if __name__ == '__main__':
    unittest.main()