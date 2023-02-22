from account_unit_tests import account_unit_tests
from message_unit_tests import message_unit_tests
from integrated_edge_tests import integrated_edge_tests
from integrated_robustness_single_client import integrated_robustness_single_client
from integrated_robustness_mult_clients import integrated_robustness_mult_clients

import sys
import socket

sys.stdout.write("Testing Wire Protocol\n")

ip = str(sys.argv[1])
port = int(sys.argv[2])
verbose = False
try: 
    verbose = bool(sys.argv[3])
except:
    pass

sys.stdout.write("Running Account Unit Tests: Test Suite 1/5\n\n")
n, p = account_unit_tests(ip, port, verbose)
sys.stdout.write(f"Test Suite 1/5: {p} out of {n} passed\n\n")

sys.stdout.write("Running Message Unit Tests: Test Suite 2/5\n\n")
n, p = message_unit_tests(ip, port, verbose)
sys.stdout.write(f"Test Suite 2/5: {p} out of {n} passed\n\n")

sys.stdout.write("Running Integrated Edge Tests: Test Suite 3/5\n\n")
n, p = integrated_edge_tests(ip, port, verbose)
sys.stdout.write(f"Test Suite 3/5: {p} out of {n} passed\n\n")

sys.stdout.write("Running Single Client Robustness Tests: Test Suite 4/5\n\n")
if (integrated_robustness_single_client(ip, port, verbose)):
    sys.stdout.write("Test Suite 4/5: All passed\n\n")

sys.stdout.write("Running Mult Client Robustness Tests: Test Suite 5/5\n\n")
if (integrated_robustness_single_client(ip, port, verbose)):
    sys.stdout.write("Test Suite 5/5: All passed\n\n")