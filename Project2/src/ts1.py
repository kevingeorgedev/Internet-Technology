import threading
import time
import random

import socket
import sys

def open_dns():
    dns_file = open("PROJ2-DNSTS1.txt", "r")
    dns = {}
    
    for line in dns_file:
        line = line.strip()
        word = line.split(' ')
        dns[word[0]] = line

    dns_file.close()
    return dns

def ts1():
    current_dns = open_dns()

    try:
        ts1s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print ("[TS1]: Top-Level Server 1 socket created")
    except socket.error as err:
        print ("[TS1]: Could not create Top-Level Server 1 socket \n Error: " + str(err))
        exit()

    ts1_binding = ("", int(sys.argv[1]))
    ts1s.bind(ts1_binding)

    ts1s.listen(5)

    ts1host = socket.gethostname()
    print("[S]: Server host name is {}".format(ts1host))
    localts1host_ip = (socket.gethostbyname(ts1host))
    print("[S]: Server IP address is {}".format(localts1host_ip))
    
    csocketid, addr = ts1s.accept()
    print ("[S]: Got a connection request from a CLIENT at {}".format(addr))

    while True:
        received_data = csocketid.recv(4096).decode("utf-8").strip()
        if not received_data:
            break
        print("[TS1]: Received message from LS: {}".format(received_data))

        if not received_data:
            break
        if received_data in current_dns:
            print("[TS1]: data SUCCESSFULLY FOUND in the DNS")
            return_statement = current_dns.get(received_data)
            csocketid.send(return_statement.encode("utf-8"))
        if received_data not in current_dns:
            print("[TS1]: data NOT FOUND in DNS")
            ############
            #empty_variable = "EMPTY_FIRST"
            #csocketid.send(empty_variable.encode("utf-8"))
            ############

    csocketid.close()
    ts1s.close()
    exit()

if __name__ == "__main__":
    ts1()

