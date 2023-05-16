import threading
import time
import random

import socket
import sys

def open_dns():
    dns_file = open("PROJ2-DNSTS2.txt", "r")
    dns = {}
    
    for line in dns_file:
        line = line.strip()
        word = line.split(' ')
        dns[word[0]] = line

    dns_file.close()
    return dns

def ts2():
    current_dns = open_dns()

    try:
        ts2s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("[TS2]: Top-Level Server 2 socket created")
    except socket.error as err:
        print ("[TS2]: Could not create Top-Level Server 2 socket \n Error: " + str(err))
        exit()

    ts2_binding = ("", int(sys.argv[1]))
    ts2s.bind(ts2_binding)

    ts2s.listen(5)

    ts2host = socket.gethostname()
    print("[S]: Server host name is {}".format(ts2host))
    localts2host_ip = (socket.gethostbyname(ts2host))
    print("[S]: Server IP address is {}".format(localts2host_ip))
    
    csocketid, addr = ts2s.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    while True:
        received_data = csocketid.recv(4096).decode("utf-8").strip()
        if not received_data:
            break
        print("[TS2]: Received message: {}".format(received_data))

        if not received_data:
            break
        if received_data in current_dns:
            print("[TS2]: data SUCCESSFULLY FOUND in the DNS")
            return_statement = current_dns.get(received_data)
            csocketid.send(return_statement.encode("utf-8"))
        if received_data not in current_dns:
            print("[TS2]: data NOT FOUND in DNS")
            ############
            #empty_variable = "EMPTY_SECOND"
            #csocketid.send(empty_variable.encode("utf-8"))
            ############

    csocketid.close()
    ts2s.close()
    exit()

if __name__ == "__main__":
    ts2()

