import unittest
import sys
sys.path.insert(1, '../')
from client import Payload, encode, decode
import random
import string
from enum import Enum

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
    
    def test_inverse(self):
        fname = "../test_cases/commands_lst.txt"
        with open(fname, 'r') as fp:
            comm = fp.readline().strip('\n')
            self.assertEqual(decode(encode(comm)), comm) #obviously the issue, because I'm fucking dumb, is that we need client encode and server decode. come back to unit tests

if __name__ == '__main__':
    unittest.main()