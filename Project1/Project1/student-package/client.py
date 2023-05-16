import socket, time

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    # Define the port on which you want to connect to the server
    port = 50006
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)

    # Send data to server
    file = open("in-proj.txt", "r")
    data = file.readlines()
    for line in data:
        cs.send(line.encode())

    # Receive data from the server
    data_from_server=cs.recv(200).decode('utf-8')

    # close the client socket
    print("[C]: Reversed text written to 'outr-proj.txt'")
    print("[C]: Uppercase text written to 'outup-proj.txt'")
    cs.close()
    exit()

if __name__ == "__main__":
    client()