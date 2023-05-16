import socket, time

def reverseFromString(data):
    msg = ""
    for i in range (len(data)):
        msg += data[i][::-1].strip()
        if i != len(data) - 1:
            msg += "\n"
    return msg

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50006)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    csockid, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    csockid.settimeout(2)
    msg = ""
    while True:
        try:
            tmp = csockid.recv(200)
            msg += tmp
            #csockid.send("".encode('utf-8'))
        except socket.timeout:
            break

    #Write message to reverse file in reverse
    file = open("outr-proj.txt", "w")
    file.write(reverseFromString(msg.split('\n')))

    #Write message to uppercase file in uppercase
    file = open("outup-proj.txt", "w")
    file.write(msg.upper())
    
    # Close the server socket
    ss.close()
    print("closed")
    exit()

if __name__ == "__main__":
    server()
