import socket
import signal
import sys
import random

# Read a command line argument for the port where the server
# must run.
port = 8080
if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    print("Using default port 8080")

# Start a listening server socket on the port
sock = socket.socket()
sock.bind(('', port))
sock.listen(2)

### Contents of pages we will serve.
# Login form
login_form = """
   <form action = "http://localhost:%d" method = "post">
   Name: <input type = "text" name = "username">  <br/>
   Password: <input type = "text" name = "password" /> <br/>
   <input type = "submit" value = "Submit" />
   </form>
""" % port
# Default: Login page.
login_page = "<h1>Please login</h1>" + login_form
# Error page for bad credentials
bad_creds_page = "<h1>Bad user/pass! Try again</h1>" + login_form
# Successful logout
logout_page = "<h1>Logged out successfully</h1>" + login_form
# A part of the page that will be displayed after successful
# login or the presentation of a valid cookie
success_page = """
   <h1>Welcome!</h1>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "password" value = "new" />
   <input type = "submit" value = "Click here to Change Password" />
   </form>
   <form action="http://localhost:%d" method = "post">
   <input type = "hidden" name = "action" value = "logout" />
   <input type = "submit" value = "Click here to logout" />
   </form>
   <br/><br/>
   <h1>Your secret data is here:</h1>
""" % (port, port)

new_password_page = """
   <form action="http://localhost:%d" method = "post">
   New Password: <input type = "text" name = "NewPassword" /> <br/>
   <input type = "submit" value = "Submit" />
</form>
""" % port

#### Helper functions
# Printing.
def print_value(tag, value):
    print ("Here is the", tag)
    print ("\"\"\"")
    print (value)
    print ("\"\"\"")
    print

# Signal handler for graceful exit
def sigint_handler(sig, frame):
    print('Finishing up by closing listening socket...')
    sock.close()
    sys.exit(0)
# Register the signal handler
signal.signal(signal.SIGINT, sigint_handler)


# TODO: put your application logic here!
# Read login credentials for all the users
# Read secret data of all the users
passwords_file = open("passwords.txt", "r")
secrets_file = open("secrets.txt", "r")
cookies_file = open("cookies.txt", "w+")

logins = {}
for line in passwords_file.readlines():
    login = line.split(" ")
    logins.update({login[0].strip() : login[1].strip()})

secrets = {}
for line in secrets_file.readlines():
    secret = line.split(" ")
    secrets.update({secret[0].strip() : secret[1].strip()})

cookies = {}

### Loop to accept incoming HTTP connections and respond.
request = False
html_content_to_send = login_page
while True:
    client, addr = sock.accept()
    req = client.recv(1024)

    # Let's pick the headers and entity body apart
    header_body = req.split('\r\n\r\n')
    headers = header_body[0]
    body = '' if len(header_body) == 1 else header_body[1]
    print_value('headers', headers)
    print_value('entity body', body)
    header_dict = {}
    arr = header_body[0].split("\r\n")
    for i in range(len(arr)):
        if(i == 0): continue
        arrsplit = arr[i].split(":")
        a = arrsplit[0].strip()
        b = arrsplit[1].strip()
        header_dict.update({a : b})
    cookie_number = ""
    if "Cookie" in header_dict:
        cookie_number = header_dict["Cookie"]

    # TODO: Put your application logic here!
    # Parse headers and body and perform various actions
    #body.

    body2 = str(body)
    body2 = body2.replace("username=", "")
    body2 = body2.replace("password=", "")
    inputs = body2.split("&")

    headers_to_send = ''

    if body == "action=logout":
        html_content_to_send = logout_page
    elif body == "password=new":
        html_content_to_send = new_password_page
    elif "NewPassword=" in body:
        logins[username] = body.replace("NewPassword=", "")
        html_content_to_send = success_page + secrets[username]
    elif cookie_number in cookies.keys():
        html_content_to_send = success_page + secrets[cookies[cookie_number]]
    elif(len(inputs) == 2):
        username = inputs[0]
        password = inputs[1]
        if username == "" and password == "":
            html_content_to_send = login_page
        elif username in logins:
            if logins[username] == password:
                html_content_to_send = success_page + secrets[username]
                rand_val = random.getrandbits(64)
                headers_to_send = "Set-Cookie: token=" + str(rand_val) + "\r\n"
                if cookie_number not in cookies:
                    cookies.update({"token=" + str(rand_val) : username})
            else:
                html_content_to_send = bad_creds_page
        else:
            html_content_to_send = bad_creds_page
            headers_to_send = ""
    else:
        html_content_to_send = login_page
        headers_to_send = ''

    # Construct and send the final response
    response  = 'HTTP/1.1 200 OK\r\n'
    response += headers_to_send
    response += 'Content-Type: text/html\r\n\r\n'
    response += html_content_to_send
    print_value('response', response)    
    client.send(response)
    client.close()
    
    print ("Served one request/connection!")
    print

# We will never actually get here.
# Close the listening socket
sock.close()
