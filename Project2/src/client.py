import threading
import time
import random

import socket
import sys


def get_queries():
    input_file = open("PROJ2-HNS.txt", "r")
    queries = input_file.read().splitlines()
    input_file.close()	
    return queries

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print ("[C]: Could not create socket \n Error: " + str(err))
        exit()

    binding_arguments = (str(sys.argv[1]), int(sys.argv[2]))
    cs.connect(binding_arguments)

    input_queries = get_queries()
    resolved_file = open("RESOLVED.txt", "w+")

    for query in input_queries:
        print ("[C]: Sent: " + query) 
        cs.send(query.encode("utf-8"))
        lsResponse = cs.recv(4096).decode("utf-8")
        print ("[C]: The received response is: "+ lsResponse) 
        resolved_file.write(lsResponse + "\n")

    resolved_file.close()
    cs.close()
    exit()

if __name__ == "__main__":
    client()
