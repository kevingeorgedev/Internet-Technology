import threading
import time
import random

import socket
import sys
import select


def create_socket():
    try:
        new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except:
        print ("[LS]: Could not create Server socket \n Error: " + str(err))
        exit()
    return new_socket

def ls():
    ls_socket = create_socket()
    ts1_socket = create_socket()
    ts2_socket = create_socket()

    ls_binding_arguments = ("", int(sys.argv[1])) 
    ts1_binding_arguments = (str(sys.argv[2]),int(sys.argv[3]))
    ts2_binding_arguments = (str(sys.argv[4]),int(sys.argv[5]))

    ls_socket.bind(ls_binding_arguments)
    ts1_socket.connect(ts1_binding_arguments)
    ts2_socket.connect(ts2_binding_arguments)

    ls_socket.listen(5)
    ts1_socket.settimeout(5)
    ts2_socket.settimeout(5)

    csocketid, addr = ls_socket.accept()
    print('[LS]: Got a connection request from: ' , addr)

######################################################################################################################################

    data_recv = ""
    while True:
        data = csocketid.recv(200).decode('utf-8')
        if not data:
            break
        print("[LS]: Received data from CLIENT: {}".format(data))

        ts1_socket.send(data.encode('utf-8'))
        ts2_socket.send(data.encode('utf-8'))

        inputs = [ts1_socket, ts2_socket]
        while inputs:
            read = False
            readers, _, _ = select.select(inputs, [], [], 5)
            for r in readers:
                print("STEP1: The data has been recovered from TS.")
                data_recv = r.recv(300).decode('utf-8')
                print("[LS]: The DNS is " + data_recv)
                read = True
                print("STEP2: The data has been sent back to the CLIENT.")
                csocketid.send(data_recv.encode('utf-8'))
                inputs.remove(r)
                break
            if read: 
                break
            if not (readers):
                print("STEP1: The data HAS NOT been recovered from either TS.")
                d = data + " - TIMED OUT"
                print("[LS] The DNS is : " + d)
                print("STEP2: The data has been sent back to the CLIENT.")
                csocketid.send(d.encode('utf-8'))
                break

    ls_socket.close()
    ts1_socket.close()
    ts2_socket.close()
    exit()


# This is a draft of the short-cut method for using select.select()
"""     data_recv = ""
    while True:
        data = csocketid.recv(4096).decode("utf-8").strip()
        if not data:
            break
        print("[LS]: Received data from CLIENT: {}".format(data))

        ts1_socket.send(data.encode("utf-8"))
        ts2_socket.send(data.encode("utf-8"))

        inputs = [ts1_socket, ts2_socket]
        readers, _, _ = select.select(inputs, [], [], 5)
        for r in readers:
            print("STEP1: The data has been recovered from TS.")
            data_recv = r.recv(4096).decode("utf-8")
            print(data_recv)
            print("STEP2: The data has been sent back to the CLIENT.")
            csocketid.send(data_recv.encode('utf-8'))
            if not data_recv:
                print("[LS]: No response from TS")
                err_str = data + " - TIMED OUT"
                csocketid.send(err_str.encode("utf-8")) """

# This is the manual method for using select.select()
""" while True:
        data = csocketid.recv(4096).decode("utf-8").strip()
        if not data:
            break
        print("[LS]: Received data from client: {}".format(data))

        ts1_socket.send(data.encode("utf-8"))
        ts2_socket.send(data.encode("utf-8"))

        try:
            ts1Data = ts1_socket.recv(4096).decode("utf-8")
            print("[LS]: Data from [TS1]: " + ts1Data)
            csocketid.send(ts1Data.encode('utf-8'))
        except socket.timeout:
            print("[LS]: No response from [TS1]")
            try:
                ts2Data = ts2_socket.recv(4096).decode("utf-8")
                print("[LS]: Data from [TS2]: {}".format(ts2Data))
                csocketid.send(ts2Data.encode("utf-8"))
            except socket.timeout:
                print("[LS]: No response from [TS2]")
                err_str = data + " - TIMED OUT"
                csocketid.send(err_str.encode("utf-8")) """

######################################################################################################################################

if __name__ == "__main__":
    ls()
